
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "modulestate.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

// parse something that might be a unicode string, bytes string or a
// name/identifier
//
// the span must be at 1 character, either 'r' or 'R'
WooshToken *
parse_unicode_bytes_or_name(WooshTokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == 'r' || review(tokenizer, 0) == 'R');
    assert(review(tokenizer, 1) == 0);

    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    switch(next_c)
    {
        case 'f':
        case 'F':
            if (!advance(tokenizer)){ return 0; }
            return parse_unicode_or_name(tokenizer);
        case 'b':
        case 'B':
            if (!advance(tokenizer)){ return 0; }
            return parse_bytes_or_name(tokenizer);
        case '\'':
        case '"':
            if (!advance(tokenizer)){ return 0; }
            return parse_string(tokenizer, 0);
        default:
            return parse_name(tokenizer);
    }
}

// parse something that might be a bytes string or a name/identifier
//
// the span must be at least 1 or 2 characters
// if 1 character, it must be either 'b' or 'B'
// if 2 characters, it must be some combination of 'b' and 'r' with any mixing
// of cases
WooshToken *
parse_bytes_or_name(WooshTokenizer *tokenizer)
{
    Py_UCS4 c_0 = review(tokenizer, 0);
    Py_UCS4 c_1 = review(tokenizer, 1);
    if (c_1 == 0)
    {
        assert(c_0 == 'b' || c_0 == 'B');
    }
    else
    {
        assert(review(tokenizer, 2) == 0);
        assert(
            ((c_0 == 'b' || c_0 == 'B') && (c_1 == 'r' || c_1 == 'R')) ||
            ((c_0 == 'r' || c_0 == 'R') && (c_1 == 'b' || c_1 == 'B'))
        );
    }

    // if our buffer just has `b` we have a unique path because it may be
    // followed by `r` and still be a bytes string
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (
        c_1 == 0 &&
        (c_0 == 'b' || c_0 == 'B') &&
        (next_c == 'r' || next_c == 'R')
    )
    {
        if (!advance(tokenizer)){ return 0; }
        c_1 = next_c;
        next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
    }
    switch(next_c)
    {
        case '\'':
        case '"':
            if (!advance(tokenizer)){ return 0; }
            return parse_string(tokenizer, 1);
        default:
            return parse_name(tokenizer);
    }
}

// parse something that might be a unicode string or a name/identifier
//
// the span must be at least 1 or 2 characters
// if 1 character, it must be either 'f', 'F', 'u' or 'U'
// if 2 characters, it must be some combination of 'f' and 'r' with any mixing
// of cases
WooshToken *
parse_unicode_or_name(WooshTokenizer *tokenizer)
{
    Py_UCS4 c_0 = review(tokenizer, 0);
    Py_UCS4 c_1 = review(tokenizer, 1);
    if (c_1 == 0)
    {
        assert(
            c_0 == 'f' || c_0 == 'F' ||
            c_0 == 'u' || c_0 == 'U'
        );
    }
    else
    {
        assert(review(tokenizer, 2) == 0);
        assert(
            ((c_0 == 'f' || c_0 == 'F') && (c_1 == 'r' || c_1 == 'R')) ||
            ((c_0 == 'r' || c_0 == 'R') && (c_1 == 'f' || c_1 == 'F'))
        );
    }

    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    // if our buffer just has `f` we have a unique path because it may be
    // followed by `r` and still be a unicode string
    if (
        c_1 == 0 &&
        (c_0 == 'f' || c_0 == 'F') &&
        (next_c == 'r' || next_c == 'R')
    )
    {
        if (!advance(tokenizer)){ return 0; }
        c_1 = next_c;
        next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
    }
    switch(next_c)
    {
        case '\'':
        case '"':
            if (!advance(tokenizer)){ return 0; }
            return parse_string(tokenizer, 0);
        default:
            return parse_name(tokenizer);
    }
}

// parse a string (which can either be a byte string or a unicode string)
//
// the span must be atleast 1 with the last character being a quote
WooshToken *
parse_string(
    WooshTokenizer *tokenizer,
    int is_bytes // 1 if this is a bytes string (otherwise a unicode string)
)
{
    Py_UCS4 quote = review_reverse(tokenizer, 0);
    assert(quote == '\'' || quote == '"');
    // determine the number of quote characters, this should be either 1 or 3
    size_t quote_count = 1;
    for (size_t i = 0; i < 2; i++)
    {
        Py_UCS4 c = peek(tokenizer, quote_count - 1);
        if (c == 0 && PyErr_Occurred()){ return 0; }
        if (c == quote){ quote_count += 1; }
        else { break; }
    }
    // it's possible that we have an empty single quoted string, which would be
    // detected as a quote count of 2
    if (quote_count == 2){ quote_count = 1; }
    // remember -- we already have the first quote in the span, so we only need
    // to advance over additional quotes
    for (size_t i = 1; i < quote_count; i++)
    {
        // TODO: add multi advance function?
        if (!advance(tokenizer)){ return 0; }
    }
    // find the end of the string
    while(1)
    {
        // search for the quote character
        int escape = 0;
        Py_UCS4 next_c;
        while(1)
        {
            next_c = peek(tokenizer, 0);
            if (next_c == 0)
            {
                if (PyErr_Occurred()){ return 0; }
                return error(tokenizer);
            }
            // bytes string literals may only contain ASCII characters
            else if (is_bytes && next_c >= 128)
            {
                if (!advance(tokenizer)){ return 0; }
                return error(tokenizer);
            }

            if (!escape)
            {
                if (next_c == quote){ break; }
                // only triple quote strings can span multiple lines
                if (next_c == '\\'){ escape = 1; }
                else if (quote_count == 1)
                {
                    if (next_c == '\n')
                    {
                        if (!advance(tokenizer)){ return 0; }
                        return error(tokenizer);
                    }
                    else if (next_c == '\r')
                    {
                        Py_UCS4 next_next_c = peek(tokenizer, 1);
                        if (next_next_c == 0 && PyErr_Occurred()){ return 0; }
                        if (next_next_c == '\n')
                        {
                            if (!advance(tokenizer)){ return 0; }
                            return error(tokenizer);
                        }
                    }
                }
            }
            else
            { escape = 0; }

            if (!advance(tokenizer)){ return 0; }
        }
        // we've found the end quote character, but for triple quotes that isn't
        // necessarily the end, we need to make sure its 3 quotes in a row
        // if not, then we restart this loop and search again
        assert(peek(tokenizer, 0) == quote);
        if (!advance(tokenizer)){ return 0; }
        size_t i;
        for (i = 1; i < quote_count; i++)
        {
            Py_UCS4 next_c = peek(tokenizer, 0);
            if (next_c == 0 && PyErr_Occurred()){ return 0; }
            if (next_c != quote){ break; }
            if (!advance(tokenizer)){ return 0; }
        }
        if (i == quote_count){ break; }
    }
    return consume(tokenizer, tokenizer->string_type, 0);
}
