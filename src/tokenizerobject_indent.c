
// this code is part of the Tokenizer, but only related to the internal parsing
// mechanics -- that is, how the source is stored in memory/discarded, how the
// tokenizer looks at the source and how the tokens are generated from it, but
// not specifically how to generate any specific token given some source text
//
// in that sense, it's lower level than the parsing portion and mostly focuses
// on efficiently shifting around and extracting the source data

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "modulestate.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

// this is the number of spaces to consider a tab for indentation, this is the
// same as CPython
#define TAB_SIZE (8)

int
init_indent(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    if (!lifo_buffer_new(&tokenizer->indent.stack, sizeof(char) * 10))
    {
        PyErr_NoMemory();
        return 0;
    }
    assert(tokenizer->indent.dedents_pending == 0);
    return 1;
}

void
dealloc_indent(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    lifo_buffer_delete(&tokenizer->indent.stack);
}

int
visit_indent(WooshTokenizer *tokenizer, visitproc visit, void *arg)
{
    assert(tokenizer);
    return 1;
}

int
clear_indent(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    return 1;
}

static size_t
get_indent(WooshTokenizer *tokenizer)
{
    if (!lifo_buffer_is_empty(&tokenizer->indent.stack))
    {
        const size_t *current_indent;
        lifo_buffer_peek(
            &tokenizer->indent.stack,
            (const void**)&current_indent,
            sizeof(size_t),
            0
        );
        return *current_indent;
    }
    return 0;
}

static WooshToken *
indent(WooshTokenizer *tokenizer, size_t line_indent)
{
    if (!lifo_buffer_push(&tokenizer->indent.stack, &line_indent, sizeof(size_t)))
    {
        return error(tokenizer);
    }
    return consume(
        tokenizer,
        tokenizer->indent_type,
        0
    );
}

static WooshToken *
dedent(WooshTokenizer *tokenizer, size_t line_indent)
{
    assert(tokenizer->indent.dedents_pending == 0);
    size_t i = 0;
    if (line_indent != 0)
    {
        const size_t *indent_p;
        while(1)
        {
            lifo_buffer_peek(
                &tokenizer->indent.stack,
                (const void **)&indent_p,
                sizeof(size_t),
                i
            );
            if (indent_p == 0)
            {
                return error(tokenizer); // unmatched dedent
            }
            if (*indent_p == line_indent){ break; }
            i += 1;
        }
    }
    else
    {
        i = lifo_buffer_count(&tokenizer->indent.stack, sizeof(size_t));
    }
    assert(i > 0);
    WooshToken *token = consume(tokenizer, tokenizer->dedent_type, 0);
    if (!token){ return 0; }
    tokenizer->indent.dedents_pending = i - 1;
    for (size_t j = 0; j < i; j ++)
    {
        lifo_buffer_pop(&tokenizer->indent.stack, sizeof(size_t));
    }
    return token;
}

WooshToken *
continue_dedent(WooshTokenizer *tokenizer)
{
    if (tokenizer->indent.dedents_pending)
    {
        WooshToken *token = consume(tokenizer, tokenizer->dedent_type, 0);
        if (!token){ return 0; }
        tokenizer->indent.dedents_pending -= 1;
        return token;
    }
    return 0;
}

WooshToken *
cleanup_dedents(WooshTokenizer *tokenizer)
{
    if (tokenizer->indent.dedents_pending == 0 &&
        !lifo_buffer_is_empty(&tokenizer->indent.stack))
    {
        return dedent(tokenizer, 0);
    }
    return continue_dedent(tokenizer);
}

// this code is part of the Tokenizer, but only related to indentation parsing
// this function determines whether to emit indent and dedent tokens, unlike
// most parse_ functions it does not return a token object, it returns a list
// of token objects or None TODO: this comment is wrong

// this function must only be called at the start of a line with span of 0
WooshToken *
parse_line_start(WooshTokenizer *tokenizer)
{
    assert(tokenizer);

#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
    fprintf(stderr, "TOKINDENT: parsing line %u start\n", tokenizer->start.line);
#endif
    int is_null = 0;
    Py_UCS4 next_c = peek_is_null(tokenizer, 0, &is_null);
    if (next_c == 0)
    {
        if (!is_null)
        {
            Py_INCREF(Py_None);
            return (WooshToken *)Py_None;
        }
        else if (PyErr_Occurred())
        {
            return 0;
        }
    }
    // whitespace makes up indents
    // we'll need to count the whitespaces and how much indent they create,
    // while moving past them
    size_t line_indent = 0;
    while(is_whitespace(next_c))
    {
        if (next_c == ' ')
        {
            line_indent += 1;
        }
        else
        {
            assert(next_c == '\t');
            line_indent += TAB_SIZE;
        }
        if (!advance(tokenizer)){ return 0; }
        next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
    }
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
    fprintf(stderr, "TOKINDENT: indent is %u\n", line_indent);
#endif
    // if we're currently in a group (parenthesis, brackets, braces)
    // then indentation cannot change
    if (peek_group(tokenizer) != 0)
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
    fprintf(stderr, "TOKINDENT: in group, indent cannot change\n");
#endif
        discard(tokenizer);
        Py_INCREF(Py_None);
        return (WooshToken *)Py_None;
    }
    // if a line is nothing but indent characters and a newline (ie.
    // there's no actual content on the line) then we don't want to
    // change indentation -- we treat it implictily like a continuation
    // of the last indent
    //
    // additionally, we don't want to emit a newline, so consume it
    if (
        next_c == '\n' ||
        (next_c == '\r' && peek(tokenizer, 1) == '\n')
    )
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
    fprintf(stderr, "TOKINDENT: line has no content, indent cannot change\n");
#endif
        if (!advance(tokenizer)){ return 0; }
        discard(tokenizer);
        Py_INCREF(Py_None);
        return (WooshToken *)Py_None;
    }
    else if (next_c == '#')
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
    fprintf(stderr, "TOKINDENT: line only has a comment, indent cannot change\n");
#endif
        discard(tokenizer);
        Py_INCREF(Py_None);
        return (WooshToken *)Py_None;
    }
    // we need to compare the indent of this line to the current indentation
    // level, so that we can see if it has changed
    size_t current_indent = get_indent(tokenizer);
    // if we've indented then we'll emit an INDENT token
    if (current_indent < line_indent)
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
        fprintf(
            stderr,
            "TOKINDENT: indenting from %u to %u\n",
            current_indent,
            line_indent
        );
#endif
        return indent(tokenizer, line_indent);
    }
    // if we've dedented then we'll need to emit some number of DEDENT
    // tokens or an error if the new indentation level is not in the stack
    else if (current_indent > line_indent)
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
        fprintf(
            stderr,
            "TOKINDENT: dedenting from %u to %u\n",
            current_indent,
            line_indent
        );
#endif
        return dedent(tokenizer, line_indent);
    }
    // the indent level might be (and often is) the same, so there is
    // nothing then to do
    else
    {
#ifdef WOOSH_TOKENIZER_DEBUG_INDENT
        fprintf(stderr, "TOKINDENT: indentation is the same\n");
#endif
        discard(tokenizer);
    }
    Py_INCREF(Py_None);
    return (WooshToken *)Py_None;
error:
    return 0;
}
