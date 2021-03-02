
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "modulestate.h"
#include "_woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

static WooshToken *
number(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    return consume(tokenizer, tokenizer->number_type, 0);
}

// parse a binary integer literal
//
// the span must be 2 and the characters must be either `0b` or `0B`
static WooshToken *
parse_binint(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '0');
    assert(
        review(tokenizer, 1) == 'b' ||
        review(tokenizer, 1) == 'B'
    );
    assert(review(tokenizer, 2) == 0);
    // the `0b` sigil must be followed by at least 1 binary number
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    Py_UCS4 next_c = 0;
    while(1)
    {
        next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_binary(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        advance(tokenizer);
        last_c = next_c;
    }
    if (last_c == '_' || !is_binary(last_c))
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        return error(tokenizer);
    }
    // note that binary integer literals may not have an exponent or imaginary
    // component
    return number(tokenizer);
}

// parse an octal integer literal
//
// the span must be 2 and the characters must be either `0o` or `0O`
static WooshToken *
parse_octint(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '0');
    assert(
        review(tokenizer, 1) == 'o' ||
        review(tokenizer, 1) == 'O'
    );
    assert(review(tokenizer, 2) == 0);
    // the `0o` sigil must be followed by at least 1 octal number that is not
    // an underscore
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_octal(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        advance(tokenizer);
        last_c = next_c;
    }
    if (last_c == '_' || !is_octal(last_c))
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        return error(tokenizer);
    }
    // note that octal integer literals may not have an exponent or imaginary
    // component
    return number(tokenizer);
}


// parse a hex integer literal
//
// the span must be 2 and the characters must be either `0x` or `0X`
static WooshToken *
parse_hexint(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '0');
    assert(
        review(tokenizer, 1) == 'x' ||
        review(tokenizer, 1) == 'X'
    );
    assert(review(tokenizer, 2) == 0);
    // the `0x` sigil must be followed by at least 1 hex number that is not
    // an underscore
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_hex(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        advance(tokenizer);
        last_c = next_c;
    }
    if (last_c == '_' || !is_hex(last_c))
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        return error(tokenizer);
    }
    return number(tokenizer);
}


// parse a number from the exponent part
//
// the last character in the buffer must be `e` or `E`
static WooshToken *
parse_exponent(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review_reverse(tokenizer, 0);
    assert(start_c == 'e' || start_c == 'E');
    // the exponent part may optionally be followed by a `+` or `-`
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case '+':
        case '-':
            if (!advance(tokenizer)){ return 0; }
            next_c = peek(tokenizer, 0);
            if (next_c == 0 && PyErr_Occurred()){ return 0; }
            break;
        default:
            break;
    }
    // after the `+` or `-` comes numbers, but the first one may not be a `_`
    if (next_c == '_')
    {
        return error(tokenizer);
    }
    // the optional `+` or `-` must be followed by a number
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_number_continue(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        if (!advance(tokenizer)){ return 0; }
        last_c = next_c;
    }
    // the exponent part must end with an actual 0-9 number
    if (last_c == '_' || !is_number_continue(last_c))
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        return error(tokenizer);
    }
    // the exponent numbers may optionally be followed by `j` or `J` to denote
    // imaginary-ness
    next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case 'j':
        case 'J':
            if (!advance(tokenizer)){ return 0; }
            break;
        default:
            break;
    }
    return number(tokenizer);
}


// parse something that is a float
//
// the last character in the span must be `.`
WooshToken *
parse_float(WooshTokenizer *tokenizer)
{
    assert(review_reverse(tokenizer, 0) == '.');
    // after the `.` comes numbers, but the first one may not be a `_`
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c == '_')
    {
        return error(tokenizer);
    }
    // a set of numbers or underscores *may* follow the `.` (0. is acceptable
    // for example)
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_number_continue(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        if (!advance(tokenizer)){ return 0; }
        last_c = next_c;
    }
    // the last character in the numbers section may not be an `_`
    if (last_c == '_')
    {
        return error(tokenizer);
    }
    // the number may be followed by an exponent or imaginary component
    next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case 'e':
        case 'E':
            if (!advance(tokenizer)){ return 0; }
            return parse_exponent(tokenizer);
        case 'j':
        case 'J':
            if (!advance(tokenizer)){ return 0; }
            break;
        default:
            break;
    }
    return number(tokenizer);
}

// parse something that starts with 0
//
// the span must be 1 and the character must be `0`
WooshToken *
parse_zero(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '0');
    assert(review(tokenizer, 1) == 0);
    for(size_t i = 0; ; i++)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        switch(next_c)
        {
            // note that for any of the non-decimal types it must be that there
            // is only one zero in the literal, otherwise it's an error
            // ex: `00x0` is not valid
            case 'b':
            case 'B':
                if (i){ return error(tokenizer); }
                if (!advance(tokenizer)){ return 0; }
                return parse_binint(tokenizer);
            case 'o':
            case 'O':
                if (i){ return error(tokenizer); }
                if (!advance(tokenizer)){ return 0; }
                return parse_octint(tokenizer);
            case 'x':
            case 'X':
                if (i){ return error(tokenizer); }
                if (!advance(tokenizer)){ return 0; }
                return parse_hexint(tokenizer);
            case 'e':
            case 'E':
                if (!advance(tokenizer)){ return 0; }
                return parse_exponent(tokenizer);
            case 'j':
            case 'J':
                if (!advance(tokenizer)){ return 0; }
                return number(tokenizer);
            case '.':
                if (!advance(tokenizer)){ return 0; }
                return parse_float(tokenizer);
            // zero may not be the start of a number
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                return error(tokenizer);
            // zero may be followed by other zeroes, just continue looping
            case '0':
                if (!advance(tokenizer)){ return 0; }
                break;
            // zero may be followed by an underscore (and another zero), again
            // continue looping
            case '_':
                if (!advance(tokenizer)){ return 0; }
                next_c = peek(tokenizer, 0);
                if (next_c == 0 && PyErr_Occurred()){ return 0; }
                if (next_c != '0')
                {
                    return error(tokenizer);
                }
                break;
            default:
                return number(tokenizer);
        }
    }
}

// parse something starting with 1-9
//
// the span must be 1 and the character must be 1-9
WooshToken *
parse_number(WooshTokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert('1' <= start_c && start_c <= '9');
    assert(review(tokenizer, 1) == 0);
    // the first number may be followed by more numbers
    Py_UCS4 last_c = start_c;
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (!is_number_continue(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        if (!advance(tokenizer)){ return 0; }
        last_c = next_c;
    }
    // the number may not end with an underscore or a non-number
    if (last_c == '_')
    {
        return error(tokenizer);
    }
    // the number may be followed by a `.`, exponent or imaginary sigil
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case '.':
            if (!advance(tokenizer)){ return 0; }
            return parse_float(tokenizer);
        case 'e':
        case 'E':
            if (!advance(tokenizer)){ return 0; }
            return parse_exponent(tokenizer);
        case 'j':
        case 'J':
            if (!advance(tokenizer)){ return 0; }
            break;
        default:
            break;
    }
    return number(tokenizer);
}
