
// this code is part of the Tokenizer, but only related to detecting the source
// encoding

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"
#include "woosh/tokenobject.h"

int
init_encoding(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->encoding.name == 0);
    assert(tokenizer->encoding.bom_offset == 0);
    return 1;
}

void
dealloc_encoding(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    Py_CLEAR(tokenizer->encoding.name);
}

// https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
static const char *UTF8_BOM = "\xEF\xBB\xBF";

enum BOM
{
    // there was some problem detecting the BOM
    BOM_ERROR,
    // there is no recognized BOM
    BOM_NONE,
    BOM_UTF8
};

// returns a BOM enum describing the BOM for the tokenizer's file-like source
static int
check_bom_file_like(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->source);
    assert(tokenizer->mechanics.readline);
    // we may need to return to the start of the source if there is no
    // detectable BOM
    PyObject *source_start = PyObject_CallMethod(tokenizer->source, "tell", 0);
    if (!source_start)
    {
        if (!PyObject_HasAttrString(tokenizer->source, "tell"))
        {
            PyErr_Format(
                PyExc_TypeError, "expected a file-like object with `tell` method (got %R)",
                tokenizer->source
            );
        }
        return 0;
    }
    // the only BOM we need to look for is the UTF8 BOM, so we'll just read
    // enough bytes from the source to check if it is there
    const size_t size_of_utf8_bom = strlen(UTF8_BOM);
    PyObject *line = PyObject_CallFunction(
        tokenizer->mechanics.readline, "n",
        size_of_utf8_bom
    );
    if (!line){ return BOM_ERROR; }
    if (!PyBytes_Check(line))
    {
        Py_DECREF(line);
        PyErr_Format(
            PyExc_TypeError, "expected %S got %S",
            &PyBytes_Type, Py_TYPE(line)
        );
        return BOM_ERROR;
    }
    if (PyBytes_GET_SIZE(line) == size_of_utf8_bom &&
        memcmp(PyBytes_AS_STRING(line), UTF8_BOM, size_of_utf8_bom) == 0)
    {
        Py_DECREF(line);
        return BOM_UTF8;
    }
    Py_DECREF(line);
    // we didn't detect a BOM, so return to the start of the source so that the
    // characters we read do not go missing from the tokenization process
    if (!PyObject_CallMethod(tokenizer->source, "seek", "O", source_start))
    {
        if (!PyObject_HasAttrString(tokenizer->source, "seek"))
        {
            PyErr_Format(
                PyExc_TypeError, "expected a file-like object with `seek` method (got %R)",
                tokenizer->source
            );
        }
        return BOM_ERROR;
    }
    return BOM_NONE;
}

// returns a BOM enum describing the BOM for the tokenizer's bytes source
static int
check_bom_bytes(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->source);
    assert(!tokenizer->mechanics.readline);
    assert(PyBytes_Check(tokenizer->source));
    // the only BOM we need to look for is the UTF8 BOM, so we'll just compare
    // the start of the byte string to check if it is there
    const size_t size_of_utf8_bom = strlen(UTF8_BOM);
    if (PyBytes_GET_SIZE(tokenizer->source) >= size_of_utf8_bom &&
        memcmp(PyBytes_AS_STRING(tokenizer->source), UTF8_BOM, size_of_utf8_bom) == 0)
    {
        tokenizer->encoding.bom_offset = size_of_utf8_bom;
        return BOM_UTF8;
    }
    return BOM_NONE;
}

// returns a BOM enum describing the BOM for the tokenizer's source
static int
check_bom(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->source);
    if (tokenizer->mechanics.readline)
    {
        return check_bom_file_like(tokenizer);
    }
    return check_bom_bytes(tokenizer);
}

enum ENCODING_COMMENT_PHASE
{
    // the encoding comment is either found or there is no encoding comment in
    // the source
    DONE,
    // currently looking for the start of the comment on the line
    SEEK_COMMENT,
    // currently looking for the 'coding' phrase of the comment
    SEEK_CODING,
    // currently looking for the '=' or ':' following the 'codding' phase of the
    // comment
    SEEK_OPERATOR,
    // currently reading the whitespace between the operator and encoding
    SEEK_ENCODING,
    // currently reading the encoding string from the comment
    READ_ENCODING,
    // indicates that the current line has no encoding comment
    NOT_FOUND
};

// returns a unicode string containing the captured encoding from the encoding
// comment or None if there is no encoding comment
//
// see: https://www.python.org/dev/peps/pep-0263/
static PyObject *
check_encoding_comment(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->source);
    PyObject *encoding = 0;
    // only the first two lines may have an encoding comment
    size_t bytes_line_start = tokenizer->encoding.bom_offset;
    for (size_t i = 0; i < 2; i++)
    {
        assert(!encoding);
        PyObject *line;
        // if we haven't found the encoding yet then the line we're looking at
        // must be utf-8 compatible, so we can decode it as such
        if (tokenizer->mechanics.readline)
        {
            line = PyFile_GetLine(tokenizer->source, 0);
            if (!line){ return 0; }
            {
                PyObject *u_line = 0;
                if (PyBytes_Check(line))
                {
                    u_line = PyUnicode_FromEncodedObject(line, "utf-8", 0);
                }
                else
                {
                    PyErr_Format(
                        PyExc_TypeError, "expected %S got %S",
                        &PyBytes_Type, Py_TYPE(line)
                    );
                }
                Py_DECREF(line);
                if (!u_line){ return 0; }
                line = u_line;
            }
            // we need to add the line to the tokenizer buffer so that it can
            // be tokenized normally later
            if (!push(tokenizer, line)){ return 0; }
            Py_INCREF(line);
        }
        else
        {
            assert(PyBytes_Check(tokenizer->source));
            const char *source = PyBytes_AS_STRING(tokenizer->source);
            size_t line_start = bytes_line_start;
            size_t line_end = line_start;
            while(1)
            {
                if (source[line_end] == '\n')
                {
                    line_end += 1;
                    break;
                }
                line_end += 1;
                if (line_end >= PyBytes_GET_SIZE(tokenizer->source))
                {
                    line_end = PyBytes_GET_SIZE(tokenizer->source);
                    break;
                }
            }
            line = PyUnicode_FromStringAndSize(
                source + line_start,
                line_end - line_start
            );
            if (!line){ return 0; }
            bytes_line_start = line_end;
        }
        // this regular expression describes how the comment must be in order
        // for it to be recognized as an encoding comment
        //
        // ^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)
        int phase = SEEK_COMMENT;
        size_t line_length = PyUnicode_GET_LENGTH(line);
        int line_kind = PyUnicode_KIND(line);
        if (line_length == 0)
        {
            Py_DECREF(line);
            break;
        }
        void *line_data = PyUnicode_DATA(line);
        size_t encoding_start_i = 0;
        size_t encoding_end_i = 0;
        for (size_t i = 0; i < line_length; i++)
        {
            Py_UCS4 c = PyUnicode_READ(line_kind, line_data, i);
            switch(phase)
            {
                // the first part of the regular expression, looking for the
                // start of the comment
                // ^[ \t\f]*#
                case SEEK_COMMENT:
                    if (c == '#')
                    {
                        phase = SEEK_CODING;
                    }
                    else if (c == '\n')
                    {
                        // nothing -- this is the end of the line anyway
                    }
                    else if (c == '\r')
                    {
                        Py_UCS4 c2 = 0;
                        if (i + 1 < line_length)
                        {
                            c2 = PyUnicode_READ(line_kind, line_data, i + 1);
                        }
                        if (c2 != '\n'){ phase = DONE; }
                    }
                    else if (c == ' ' || c == '\t' || c == '\f')
                    {
                        phase = DONE;
                    }
                    break;
                // the second part of the regular expression, looking for the
                // "coding" phrase
                // .*?coding
                case SEEK_CODING:
                    // 7 because there must be enough characters left to have
                    // "coding", the operator ("=" or ":") and at least one
                    // character for the encoding itself
                    if (i + 7 > line_length)
                    {
                        phase = NOT_FOUND;
                    }
                    else if (
                        c == 'c' &&
                        PyUnicode_READ(line_kind, line_data, i + 1) == 'o' &&
                        PyUnicode_READ(line_kind, line_data, i + 2) == 'd' &&
                        PyUnicode_READ(line_kind, line_data, i + 3) == 'i' &&
                        PyUnicode_READ(line_kind, line_data, i + 4) == 'n' &&
                        PyUnicode_READ(line_kind, line_data, i + 5) == 'g'
                    )
                    {
                        phase = SEEK_OPERATOR;
                        i += 5;
                    }
                    break;
                // the third part of the regular expression, looking for the
                // operator following the "coding" phrase
                // [:=]
                case SEEK_OPERATOR:
                    if (c != '=' && c != ':')
                    {
                        // we switch back to the "coding" mode if it wasn't
                        // followed by the correct operator, ie:
                        //  # codingcoding=utf-8
                        // is valid as utf-8
                        phase = SEEK_CODING;
                    }
                    else
                    {
                        phase = SEEK_ENCODING;
                    }
                    break;
                // the fourth part of the regular expression, looking for the
                // start of the encoding characters
                // [ \t]*
                case SEEK_ENCODING:
                    if (c != ' ' && c != '\t')
                    {
                        phase = READ_ENCODING;
                        encoding_start_i = i;
                    }
                    else
                    {
                        break;
                    }
                    // NOTE: intentionally falling through to READ_ENCODING
                    assert(phase == READ_ENCODING);
                // the last part of the regular expression, reading the encoding
                // itself
                // ([-_.a-zA-Z0-9]+)
                case READ_ENCODING:
                    if (!(
                        c == '-' || c == '_' || c == '.' ||
                        (c >= 'a' && c <= 'z') ||
                        (c >= 'A' && c <= 'Z') ||
                        (c >= '0' && c <= '9')
                    ))
                    {
                        if (encoding_start_i >= encoding_end_i)
                        {
                            // again we can switch back to "coding" mode if the
                            // encoding part is empty, ie:
                            //  # coding==coding=utf-8
                            // is valid as utf-8
                            phase = SEEK_CODING;
                        }
                        else
                        {
                            phase = DONE;
                        }
                    }
                    else
                    {
                        encoding_end_i = i + 1;
                        if (encoding_end_i == line_length)
                        {
                            phase = DONE;
                        }
                    }
                    break;
            }
            if (phase == DONE || phase == NOT_FOUND){ break; }
        }
        // if we've found an encoding comment then we don't need to continue
        // looking for another one
        if (phase == DONE)
        {
            if (encoding_start_i < encoding_end_i)
            {
                assert(!encoding);
                encoding = PyUnicode_Substring(
                    line,
                    encoding_start_i,
                    encoding_end_i
                );
                if (!encoding)
                {
                    // LCOV_EXCL_START
                    Py_DECREF(line);
                    return 0;
                    // LCOV_EXCL_STOP
                }
            }
            Py_DECREF(line);
            break;
        }
        Py_DECREF(line);
    }
    if (!encoding)
    {
        Py_INCREF(Py_None);
        encoding = Py_None;
    }
    return encoding;
}

// generates the ENCODING token based off the BOM and encoding comment
//
// may also generate an ERROR token if the BOM and encoding comment conflict
static WooshToken *
reconcile_bom_and_encoding_comment(
    WooshTokenizer *tokenizer,
    int bom,
    PyObject *encoding_comment
)
{
    assert(bom != BOM_ERROR);
    assert(encoding_comment);

    WooshType *token_type = tokenizer->encoding_type;
    PyObject *token_value = 0;
    // we need to check that the BOM and encoding comment match -- or produce
    // an error if they do not
    if (bom == BOM_UTF8 && encoding_comment != Py_None)
    {
        PyObject *encoding_comment_lower = PyObject_CallMethod(
            encoding_comment, "lower", 0
        );
        if (!encoding_comment_lower){ return 0; }
        PyObject *ascii_encoding_comment = PyUnicode_AsASCIIString(
            encoding_comment_lower
        );
        Py_DECREF(encoding_comment_lower);
        if (!ascii_encoding_comment){ return 0; }
        char *c_encoding_comment = PyBytes_AS_STRING(ascii_encoding_comment);
        if (
            strcmp(c_encoding_comment, "utf-8") != 0 &&
            strcmp(c_encoding_comment, "utf8") != 0
        )
        {
            token_type = tokenizer->error_type;
            token_value = PyUnicode_FromFormat(
                "encoding comment %R does not match BOM (utf-8)",
                encoding_comment
            );
            if (!token_value)
            {
                // LCOV_EXCL_START
                Py_DECREF(ascii_encoding_comment);
                return 0;
                // LCOV_EXCL_STOP
            }
        }
        Py_DECREF(ascii_encoding_comment);
    }
    // the default encoding it utf-8 if no BOM or encoding comment was specified
    if (encoding_comment == Py_None)
    {
        assert(token_value == 0);
        token_value = PyUnicode_FromString("utf-8");
        if (!token_value){ return 0; }
    }
    else if (token_value == 0)
    {
        Py_INCREF(encoding_comment);
        token_value = encoding_comment;
    }

    assert(token_type);
    assert(token_value);
    Py_INCREF(token_type);
    PyObject *zero = PyLong_FromLong(0);
    Py_INCREF(zero);
    PyObject *one = PyLong_FromLong(1);
    Py_INCREF(one);
    return WooshToken_NEW(
        tokenizer->token,
        token_type, token_value,
        one, zero,
        one, zero
    );
}

const char *
encoding(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    if (!tokenizer->encoding.name){ return 0; }
    return PyBytes_AS_STRING(tokenizer->encoding.name);
}

// this should be the first parse function called by the tokenizer, it will
// generate the ENCODING comment and set the appropriate encoding on the
// tokenizer so that the rest of the parsing machinery uses the correct decoder
WooshToken *
parse_encoding(WooshTokenizer *tokenizer)
{
    assert(tokenizer->encoding.name == 0);

    int bom = check_bom(tokenizer);
    if (bom == BOM_ERROR){ return 0; }

    PyObject *encoding_comment = check_encoding_comment(tokenizer);
    if (!encoding_comment){ return 0; }

    WooshToken *token = reconcile_bom_and_encoding_comment(
        tokenizer,
        bom,
        encoding_comment
    );
    Py_DECREF(encoding_comment);
    if (!token){ return 0; }
    // the encoding will always be ascii compatible and we need a char* version
    // of the encoding to use the decoder functions, so convert the token value
    // (which should be a python API compatible encoding name) to bytes and
    // store it on the tokenizer for later
    if (WooshToken_GET_TYPE(token) == tokenizer->encoding_type)
    {
        tokenizer->encoding.name = PyUnicode_AsASCIIString(
            (PyObject *)WooshToken_GET_VALUE(token)
        );
        if (!tokenizer->encoding.name)
        {
            // LCOV_EXCL_START
            Py_DECREF(token);
            return 0;
            // LCOV_EXCL_STOP
        }
        // check that the encoding can be used to decode a byte string
        {
            PyObject *s = PyUnicode_Decode(
                "", 1,
                PyBytes_AS_STRING(tokenizer->encoding.name), 0
            );
            if (s){ Py_DECREF(s); }
            else
            {
                Py_DECREF(token);
                PyErr_Clear();
                return error_format(
                    tokenizer,
                    "invalid encoding: %R",
                    tokenizer->encoding.name
                );
            }
        }
    }
    return token;
}
