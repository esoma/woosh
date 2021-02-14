
// this code is part of the Tokenizer, but only related to the parsing of group
// tokens (parenthesis, brackets and braces)
//
// the tokenizer maintains a stack where the top most item on the stack is the
// most recently opened group, when a close group character is found it is
// matched against the current (top most) group token on the stack
//
// indentation behavior also changes based on whether we're in a group or not
// (indentation does not change while inside a group)

// TODO: the token values can be cached on the module and reused, rather than
// generating new strings from the source -- this should be a memory and speed
// improvement

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "lifobuffer.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

int
init_groups(WooshTokenizer *tokenizer)
{
    assert(tokenizer);

    if (!lifo_buffer_new(&tokenizer->groups.stack, sizeof(char) * 10))
    {
        PyErr_NoMemory();
        return 0;
    }

    return 1;
}

void
dealloc_groups(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    lifo_buffer_delete(&tokenizer->groups.stack);
}

// push a group character onto the stack
// returns a truthy value on success, returns a falsey value if there was a
// memory error (this does not set a python exception)
static int
push_group(WooshTokenizer *tokenizer, char c)
{
    assert(tokenizer);
    assert(c == '(' || c == '[' || c == '{');
    return lifo_buffer_push(&tokenizer->groups.stack, &c, sizeof(char));
}

// remove the top group character from the stack
static void
pop_group(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(!lifo_buffer_is_empty(&tokenizer->groups.stack));
    lifo_buffer_pop(&tokenizer->groups.stack, sizeof(char));
}

// look at the group character on the top of the stack
// returns 0 if the stack is empty
char
peek_group(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    const char *c;
    lifo_buffer_peek(&tokenizer->groups.stack, (const void **)&c, sizeof(char), 0);
    if (c == 0){ return 0; }
    return *c;
}

// parse an operator which starts a group
//
// the only character in the span must be a `(`, `[` or `{`
WooshToken *
parse_open_operator(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c == '(' || start_c == '[' || start_c == '{');
    assert(review(tokenizer, 1) == 0);
    if (!push_group(tokenizer, start_c))
    {
        PyErr_NoMemory();
        return 0;
    }
    return operator(tokenizer);
}

// parse an operator which ends a group
//
// the only character in the span must be a `)`, `]` or `}`
WooshToken *
parse_close_operator(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c == ')' || start_c == ']' || start_c == '}');
    assert(review(tokenizer, 1) == 0);
    // a close token that doesn't match the current open token is unexpected
    char open_c = peek_group(tokenizer);
    if (open_c == 0)
    {
        return error(tokenizer); // TODO: unexpected close token
    }
    Py_UCS4 match_c;
    switch(open_c)
    {
        case '(':
            match_c = ')';
            break;
        case '[':
            match_c = ']';
            break;
        case '{':
            match_c = '}';
            break;
        default:
            assert(0);
            break;
    }
    if (start_c != match_c)
    {
        return error(tokenizer); // TODO: close token does not match
    }
    pop_group(tokenizer);
    return operator(tokenizer);
}
