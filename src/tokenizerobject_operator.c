
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "modulestate.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

// parse something starting with a '.'
//
// the span must be 1 and the only character in the span must be a `.`
WooshToken *
parse_dot(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '.');
    assert(review(tokenizer, 1) == 0);

    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    // the ellipsis (...) will always be composed of three consecutive dots
    if (next_c == '.')
    {
        Py_UCS4 next_next_c = peek(tokenizer, 1);
        if (next_next_c == 0 && PyErr_Occurred()){ return 0; }
        if (next_next_c == '.')
        {
            if (!advance(tokenizer) || !advance(tokenizer)){ return 0; }
        }
    }
    // a dot that is followed by a number (0-9) is a float
    else if (is_number_start(next_c))
    {
        return parse_float(tokenizer);
    }
    // `.` or `...`
    return operator(tokenizer);
}

// parse an operator that may be followed by an `=`
//
// for example the character `+` may be either `+` or `+=`
// also the set of characters `**` may be either `**` or `**=`
//
// the span must be atleast 1
WooshToken *
parse_operator_equal_follows(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c == '=')
    {
        if (!advance(tokenizer)){ return 0; }
    }
    return operator(tokenizer);
}

// parse an operator that may be followed by itself, itself and an `=` or just
// and '='
//
// for example the character `*` may be either `*`, `**`, `*=`, or `**=`
//
// the span must be 1 and the only character
WooshToken *
parse_operator_double_equal_follows(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c != 0);
    assert(review(tokenizer, 1) == 0);
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c == start_c)
    {
        if (!advance(tokenizer)){ return 0; }
    }
    return parse_operator_equal_follows(tokenizer);
}

// parse something starting with a `<`
//
// the span must be 1 and the only character in the span must be a `<`
WooshToken *
parse_less_than(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '<');
    assert(review(tokenizer, 1) == 0);
    // `<` is either `<` `<<`, `<>`, `<=` or `<<=`
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case '>':
        case '=':
            if (!advance(tokenizer)){ return 0; }
            break;
        case '<':
            if (!advance(tokenizer)){ return 0; }
            Py_UCS4 next_next_c = peek(tokenizer, 0);
            if (next_next_c == 0 && PyErr_Occurred()){ return 0; }
            if (next_next_c == '=')
            {
                if (!advance(tokenizer)){ return 0; }
            }
            break;
        default:
            break;
    }
    return operator(tokenizer);
}

// parse something starting with a `-`
//
// the span must be 1 and the only character in the span must be a `-`
WooshToken *
parse_minus(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '-');
    assert(review(tokenizer, 1) == 0);
    // `-` is either `-` `->` or `-=`
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c == '>' || next_c == '=')
    {
        if (!advance(tokenizer)){ return 0; }
    }
    return operator(tokenizer);
}

// parse something start with `!`
//
// the span must be 1 and the only character in the span must be a `!`
WooshToken *
parse_bang(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '!');
    assert(review(tokenizer, 1) == 0);
    // the `!` character must be immediatley followed by a `=` character to make
    // the `!=` operator token
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c != '=')
    {
        return error(tokenizer);
    }
    if (!advance(tokenizer)){ return 0; }
    return operator(tokenizer);
}

WooshToken *
operator(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    return consume(tokenizer, tokenizer->operator_type, 0);
}
