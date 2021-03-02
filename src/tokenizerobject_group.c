
// this code is part of the Tokenizer, but only related to the parsing of group
// tokens (parenthesis, brackets and braces)
//
// the tokenizer maintains a stack where the top most item on the stack is the
// most recently opened group, when a close group character is found it is
// matched against the current (top most) group token on the stack
//
// indentation behavior also changes based on whether we're in a group or not
// (indentation does not change while inside a group)

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "lifobuffer.h"
#include "_woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

int
init_groups(WooshTokenizer *tokenizer)
{
    assert(tokenizer);

    if (!lifo_buffer_new(&tokenizer->groups.stack, sizeof(char) * 10))
    {
        // LCOV_EXCL_START
        PyErr_NoMemory();
        return 0;
        // LCOV_EXCL_STOP
    }
    
    tokenizer->groups.lpar = PyUnicode_FromString("(");
    if (!tokenizer->groups.lpar){ return 0; }
    tokenizer->groups.rpar = PyUnicode_FromString(")");
    if (!tokenizer->groups.rpar){ return 0; }
    
    tokenizer->groups.lsqr = PyUnicode_FromString("[");
    if (!tokenizer->groups.lsqr){ return 0; }
    tokenizer->groups.rsqr = PyUnicode_FromString("]");
    if (!tokenizer->groups.rsqr){ return 0; }
    
    tokenizer->groups.lbrc = PyUnicode_FromString("{");
    if (!tokenizer->groups.lbrc){ return 0; }
    tokenizer->groups.rbrc = PyUnicode_FromString("}");
    if (!tokenizer->groups.rbrc){ return 0; }

    return 1;
}

void
dealloc_groups(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    lifo_buffer_delete(&tokenizer->groups.stack);
    
    Py_CLEAR(tokenizer->groups.lpar);
    Py_CLEAR(tokenizer->groups.rpar);
    
    Py_CLEAR(tokenizer->groups.lsqr);
    Py_CLEAR(tokenizer->groups.rsqr);
    
    Py_CLEAR(tokenizer->groups.lbrc);
    Py_CLEAR(tokenizer->groups.rbrc);
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
void
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
        // LCOV_EXCL_START
        PyErr_NoMemory();
        return 0;
        // LCOV_EXCL_STOP
    }
    switch(start_c)
    {
        case '(':
            return operator_value(tokenizer, tokenizer->groups.lpar);
        case '[':
            return operator_value(tokenizer, tokenizer->groups.lsqr);
        case '{':
            return operator_value(tokenizer, tokenizer->groups.lbrc);
    }
    // LCOV_EXCL_START
    assert(0);
    return 0;
    // LCOV_EXCL_STOP
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
        // LCOV_EXCL_START
        default:
            assert(0);
            break;
        // LCOV_EXCL_STOP
    }
    if (start_c != match_c)
    {
        return error(tokenizer); // TODO: close token does not match
    }
    pop_group(tokenizer);
    // we're using open_c here instead of start_c because (I believe?) the
    // compiler can more easily optimize this
    switch(open_c)
    {
        case '(':
            return operator_value(tokenizer, tokenizer->groups.rpar);
        case '[':
            return operator_value(tokenizer, tokenizer->groups.rsqr);
        case '{':
            return operator_value(tokenizer, tokenizer->groups.rbrc);
    }
    // LCOV_EXCL_START
    assert(0);
    return 0;
    // LCOV_EXCL_STOP
}
