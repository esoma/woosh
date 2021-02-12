
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "modulestate.h"
#include "tokenizerobject.h"
#include "tokenizerobject_internal.h"
#include "tokenobject.h"

int
init_parse(WooshTokenizer *tokenizer)
{
    assert(tokenizer);

    assert(tokenizer->parse.is_in_line_continuation == 0);
    assert(tokenizer->parse.last_token_type == 0);
    assert(tokenizer->parse.eof_newline == 0);
    assert(tokenizer->parse.endmarker == 0);

    return 1;
}

void
dealloc_parse(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
}

int
visit_parse(WooshTokenizer *tokenizer, visitproc visit, void *arg)
{
    assert(tokenizer);
    return 1;
}

int
clear_parse(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    return 1;
}

// parse a newline character
//
// the span must either be `\n` or `\r\n`
static WooshToken *
parse_newline(WooshTokenizer *tokenizer)
{
    assert(
        (review(tokenizer, 0) == '\n' && review(tokenizer, 1) == 0) ||
        (
            review(tokenizer, 0) == '\r' &&
            review(tokenizer, 1) == '\n' &&
            review(tokenizer, 2) == 0
        )
    );
    tokenizer->parse.is_in_line_continuation = 0;
    // we only emit a NEWLINE token when we're not currently in a group (that
    // is within parenthesis, brackets or braces)
    if (peek_group(tokenizer) == 0)
    {
        return consume(tokenizer, tokenizer->newline_type, 0);
    }
    discard(tokenizer);
    Py_INCREF(Py_None);
    return (WooshToken *)Py_None;
}

// parse whitespace
//
// the span must be 1 and the only character in the span must be whitespace
static WooshToken *
parse_whitespace(WooshTokenizer *tokenizer)
{
    assert(is_whitespace(review(tokenizer, 0)));
    assert(review(tokenizer, 1) == 0);
    // discard all the whitespace that comes after the initial whitespace
    // character
    while(1)
    {
        Py_UCS4 c = peek(tokenizer, 0);
        if (c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_whitespace(c)){ break; }
        if (!advance(tokenizer)){ return 0; }
    }
    discard(tokenizer);
    Py_INCREF(Py_None);
    return (WooshToken *)Py_None;
}

// parse an `\` character, which causes a line continuation
//
// the span must be 1 and the only character in the span must be a `\`
//
// note that this is unlike most parse functions as it may return None instead
// of a token object
static WooshToken *
parse_continuation(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '\\');
    assert(review(tokenizer, 1) == 0);
    // we don't want to tokenize the continuation character itself
    discard(tokenizer);
    // strip everything after the continuation character, there should only be
    // whitespace between the continuation character and the newline
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0)
        {
            if (PyErr_Occurred()){ return 0; }
            break;
        }
        else if (next_c == '\n')
        {
            break;
        }
        else if (next_c == '\r')
        {
            Py_UCS4 next_next_c = peek(tokenizer, 1);
            if (next_next_c == 0 && PyErr_Occurred()){ return 0; }
            if (next_next_c == '\n')
            {
                break;
            }
        }
        if (!is_whitespace(next_c))
        {
            return error(tokenizer);
        }
        advance(tokenizer);
    }
    tokenizer->parse.is_in_line_continuation = 1;
    // strip out the newline
    advance(tokenizer);
    discard(tokenizer);

    Py_INCREF(Py_None);
    return (WooshToken *)Py_None;
}

// parse a `#` character and the remaining line as a comment
//
// the only character in the span must be a `#`
static WooshToken *
parse_comment(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '#');
    assert(review(tokenizer, 1) == 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0)
        {
            if (PyErr_Occurred()){ return 0; }
            break;
        }
        else if (next_c == '\n')
        {
            break;
        }
        else if (next_c == '\r')
        {
            Py_UCS4 next_next_c = peek(tokenizer, 1);
            if (next_next_c == 0 && PyErr_Occurred()){ return 0; }
            if (next_next_c == '\n')
            {
                break;
            }
        }
        if (!advance(tokenizer)){ return 0; }
    }
    return consume(tokenizer, tokenizer->comment_type, 0);
}

// parse something that is a name/identifier
//
// the start character must be a character that a name may start with
// the remaining characters in the span must be characters that a name may
// continue with
WooshToken *
parse_name(WooshTokenizer *tokenizer)
{
    assert(is_name_start(review(tokenizer, 0)));
    for(size_t i = 1;; i++)
    {
        Py_UCS4 continue_c = review(tokenizer, i);
        if (continue_c == 0){ break; }
        assert(is_name_continue(continue_c));
    }
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_name_continue(next_c)){ break; }
        if (!advance(tokenizer)){ return 0; }
    }
    return consume(tokenizer, tokenizer->name_type, 0);
}

// parse the next token, assuming that the tokenization logic for a line start
// has already been done (parse_line_start)
//
// the span must contain exactly 1 character or the character combination `\r\n`
// or be empty due to eof or a null byte
static WooshToken *
parse_line_continue(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    if (start_c == 0)
    {
        // start_c being 0 can either mean we have no further data to process
        // or that the next byte is actually null
        //
        // a null byte is an error token while an empty buffer just means we
        // can continue doing other stuff
        int is_null = 0;
        Py_UCS4 next_c = peek_is_null(tokenizer, 0, &is_null);
        assert(next_c == 0);
        if (is_null)
        {
            if (!advance_over_null(tokenizer, 1)){ return 0; }
            return error_format(tokenizer, "%c", 0);
        }
        Py_INCREF(Py_None);
        return (WooshToken *)Py_None;
    }
    assert(
        (start_c != 0 && review(tokenizer, 1) == 0) ||
        (
            start_c =='\r' &&
            review(tokenizer, 1) == '\n' &&
            review(tokenizer, 2) == 0
        )
    );
    switch(start_c)
    {
        case '\r':
            // \r is a weird case, we always advance over \r\n in one go, so
            // if \r is the only character in the span then \r isn't being
            // followed by \n
            //
            // since \r doesn't mean anything by itself we'll make this a unique
            // error
            if (review(tokenizer, 1) == 0)
            {
                return error(tokenizer);
            }
            // intentionally falling through to /n
        case '\n':
            return parse_newline(tokenizer);
        case ' ':
        case '\t':
            return parse_whitespace(tokenizer);
        case '.':
            return parse_dot(tokenizer);
        case '+':
        case '@':
        case '%':
        case '^':
        case '&':
        case '|':
        case ':':
        case '=':
            return parse_operator_equal_follows(tokenizer);
        case '*':
        case '/':
        case '>':
            return parse_operator_double_equal_follows(tokenizer);
        case '<':
            return parse_less_than(tokenizer);
        case '-':
            return parse_minus(tokenizer);
        case '!':
            return parse_bang(tokenizer);
        case '(':
        case '[':
        case '{':
            return parse_open_operator(tokenizer);
        case ')':
        case ']':
        case '}':
            return parse_close_operator(tokenizer);
        case '\\':
            return parse_continuation(tokenizer);
        case '#':
            return parse_comment(tokenizer);
        case '~':
        case ',':
        case ';':
            return operator(tokenizer);
        case '0':
            return parse_zero(tokenizer);
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
        case '6':
        case '7':
        case '8':
        case '9':
            return parse_number(tokenizer);
        case 'r':
        case 'R':
            return parse_unicode_bytes_or_name(tokenizer);
        case 'b':
        case 'B':
            return parse_bytes_or_name(tokenizer);
        case 'u':
        case 'U':
        case 'f':
        case 'F':
            return parse_unicode_or_name(tokenizer);
        case '\'':
        case '"':
            return parse_string(tokenizer, 0);
        default:
            if (is_name_start(start_c))
            {
                return parse_name(tokenizer);
            }
            break;
    }
    return error(tokenizer);
}

static WooshToken *
yield_token(WooshTokenizer *tokenizer, WooshToken *token)
{
    assert(tokenizer);
    if (token)
    {
        tokenizer->parse.last_token_type = WooshToken_GET_TYPE(token);
    }
    return token;
}

WooshToken *
parse(WooshTokenizer *tokenizer)
{
again:
    if (tokenizer->parse.last_token_type != tokenizer->error_type)
    {
        if (encoding(tokenizer) == 0)
        {
            return yield_token(tokenizer, parse_encoding(tokenizer));
        }
        {
            WooshToken *dedent = continue_dedent(tokenizer);
            if (dedent){ return dedent; }
            else if (PyErr_Occurred()){ return 0; }
        }

        if (end_column(tokenizer) == 0 &&
            !tokenizer->parse.is_in_line_continuation)
        {
            size_t line = end_line(tokenizer);
            WooshToken *token = parse_line_start(tokenizer);
            if (!token){ return 0; }
            if ((PyObject *)token != Py_None){ return yield_token(tokenizer, token); }
            Py_CLEAR(token);
            if (line != end_line(tokenizer)){ goto again; }
        }

        if (!advance(tokenizer)){ return 0; }
        WooshToken *token = parse_line_continue(tokenizer);
        if (!token){ return 0; }
        if ((PyObject *)token != Py_None){ return yield_token(tokenizer, token); }
        Py_CLEAR(token);
        if (!at_eof(tokenizer)){ goto again; }

        char open_group = peek_group(tokenizer);
        if (open_group != 0)
        {
            char close_group = 0;
            switch(open_group)
            {
                case '(':
                    close_group = ')';
                    break;
                case '[':
                    close_group = ']';
                    break;
                case '{':
                    close_group = '}';
                    break;
                default:
                    assert(0);
            }
            return yield_token(tokenizer, error_format(
                tokenizer,
                "unexpected end of file, expected '%c'",
                close_group
            ));
        }

        if (!tokenizer->parse.eof_newline)
        {
            tokenizer->parse.eof_newline = 1;
            if (tokenizer->parse.last_token_type != tokenizer->newline_type)
            {
                return yield_token(tokenizer, consume(tokenizer, tokenizer->newline_type, 0));
            }
        }
        // dedent back to 0
        {
            WooshToken *dedent = cleanup_dedents(tokenizer);
            if (dedent){ return yield_token(tokenizer, dedent); }
            else if (PyErr_Occurred()){ return 0; }
        }
        // end with an EOF token
        if (!tokenizer->parse.endmarker)
        {
            tokenizer->parse.endmarker = 1;
            return yield_token(tokenizer, consume(tokenizer, tokenizer->eof_type, 0));
        }
    }

    return 0;
}
