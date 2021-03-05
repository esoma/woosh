
// this code is part of the Tokenizer, but only related to finding if a given
// character is part of some defined set of characters

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "unicode.h"

int
is_whitespace(Py_UCS4 c)
{
    return c == ' ' || c == '\t';
}

// indicates that the character can start a number
int
is_number_start(Py_UCS4 c)
{
    return '0' <= c && c <= '9';
}

// indicates that the character can be part of the continuation of a number
int
is_number_continue(Py_UCS4 c)
{
    return is_number_start(c) || c == '_';
}

// indicates that the character can be the binary part of the number following
// the 0b part of the literal
int
is_binary(Py_UCS4 c)
{
    return '0' == c || c == '1' || c == '_';
}

// indicates that the character can be the octal part of the number following
// the 0o part of the literal
int
is_octal(Py_UCS4 c)
{
    return ('0' <= c && c <= '7') || c == '_';
}

// indicates that the character can be the hex part of the number following the
// 0x part of the literal
int
is_hex(Py_UCS4 c)
{
    return (
        ('0' <= c && c <= '9') ||
        ('a' <= c && c <= 'f') ||
        ('A' <= c && c <= 'F') ||
        c == '_'
    );
}

// determines if the character can be the start of a name (identifier)
// any unicode character with the XID_START property
int
is_name_start(Py_UCS4 c)
{
    // technically this is unicode codepoints with the property `XID_START`, but
    // we create a fast path for ascii characters, which would be the most
    // common
    return (
        ('a' <= c && c <= 'z') ||
        ('A' <= c && c <= 'Z') ||
        c == '_' ||
        // non-ascii characters
        (c > 127 && is_unicode_xid_start(c))
    );
}

// determines if the character can be part of the continuation of a name
// (identifier)
// any unicode character with the XID_CONTINUE property
int
is_name_continue(Py_UCS4 c)
{
    // technically this is unicode codepoints with the property `XID_CONTINUE`,
    // but we create a fast path for ascii characters, which would be the most
    // common
    return (
        ('0' <= c && c <= '9') ||
        ('a' <= c && c <= 'z') ||
        ('A' <= c && c <= 'Z') ||
        c == '_' ||
        // non-ascii characters
        (c > 127 && is_unicode_xid_continue(c))
    );
}
