
// this code is part of the Tokenizer, but only related to the internal parsing
// mechanics -- that is, how the source is stored in memory/discarded, how the
// tokenizer looks at the source and how the tokens are generated from it, but
// not specifically how to generate any specific token given some source text
//
// it's lower level than the parsing portion and mostly focuses on efficiently
// shifting around and extracting the source data

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "fifobuffer.h"
#include "modulestate.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

int
init_mechanics(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    if (!fifo_buffer_new(
        &tokenizer->mechanics.buffer,
        sizeof(PyObject *) * 10
    ))
    {
        PyErr_NoMemory();
        return 0;
    }
    tokenizer->mechanics.start.line = 1;
    assert(tokenizer->mechanics.start.column == 0);
    assert(tokenizer->mechanics.start.line_index == 0);
    assert(tokenizer->mechanics.start.character_index == 0);
    tokenizer->mechanics.end.line = 1;
    assert(tokenizer->mechanics.end.column == 0);
    assert(tokenizer->mechanics.end.line_index == 0);
    assert(tokenizer->mechanics.end.character_index == 0);
    return 1;
}

void
dealloc_mechanics(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    // deallocate the buffer, making sure to decref any lines that are still
    // stored in it
    PyObject *start;
    PyObject *end;
    fifo_buffer_read(
        &tokenizer->mechanics.buffer,
        (void **)&start, (void **)&end
    );
    if (start)
    {
        assert(end);
        for (PyObject *line = start; start < end; start++)
        {
            Py_DECREF(line);
        }
        fifo_buffer_delete(&tokenizer->mechanics.buffer);
    }
}

// reads the next line from the source and puts it in the buffer
//
// returns a truthy value on success, returns falsey if there was an error and
// sets the python exception
static int
load_line(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->source);
    assert(encoding(tokenizer));
    if (tokenizer->mechanics.eof){ return 1; }
    // TODO: make the line size customizeable and allow full read?
    PyObject *line = PyFile_GetLine(tokenizer->source, 1024);
    if (!PyBytes_Check(line))
    {
        PyErr_Format(
            PyExc_TypeError, "expected %S got %S",
            &PyBytes_Type, Py_TYPE(line)
        );
        Py_DECREF(line);
        return 0;
    }
    if (PyBytes_GET_SIZE(line) == 0)
    {
        tokenizer->mechanics.eof = 1;
        return 1;
    }
    if (!line){ return 0; }
    {
        PyObject *u_line = PyUnicode_FromEncodedObject(
            line,
            encoding(tokenizer),
            0
        );
        Py_DECREF(line);
        if (!u_line){ return 0; }
        line = u_line;
    }
    if (!push(tokenizer, line))
    {
        Py_DECREF(line);
        return 0;
    }
    return 1;
}

// returns the next character (+ offset) that `advance` would add to the token
// we're currently building
//
// so offset of 0 would show the next character, offset of 1 would show the
// one after that, etc...
//
// return 0 if looking beyond the end of the source, if a null byte was
// encountered, or if there was an error
//
// use PyErr_Occurred() to check if an error was set if 0 is returned
//
// is_null may be optionally supplied to inform whether the returned byte is
// actually null or if the end of the source was encountered; typically this
// information is not needed so `peek` is used instead
Py_UCS4
peek_is_null(WooshTokenizer *tokenizer, size_t offset, int *is_null)
{
    assert(tokenizer);
    // find the line that holds the token just outside the span
    PyObject **start;
    PyObject **end;
    fifo_buffer_read(
        &tokenizer->mechanics.buffer,
        (void **)&start,
        (void **)&end
    );
    // it could be that the current span ends right at the end of the last line
    // in the buffer, so we'll need to immediatley load the next line if so
    PyObject **line = start + tokenizer->mechanics.end.line_index;
    if (line >= end)
    {
        if (!load_line(tokenizer)){ return 0; }
        fifo_buffer_read(
            &tokenizer->mechanics.buffer,
            (void **)&start,
            (void **)&end
        );
        line = start + tokenizer->mechanics.end.line_index;
        if (line >= end){ return 0; }
    }
    // we need to adjust the offset based on how far we've read into this last
    // line
    offset += tokenizer->mechanics.end.character_index;
    // our offset may push us into a different line, so iterate over the lines
    // and adjust our offset until we find one that contains the character we're
    // looking for (or until the source expires)
    while(1)
    {
        size_t line_length = PyUnicode_GET_LENGTH(*line);
        if (line_length > offset){ break; }
        offset -= line_length;
        line += 1;
        if (line >= end)
        {
            // we've reached the end of the currently loaded source, try to load
            // another line
            if (!load_line(tokenizer)){ return 0; }
            fifo_buffer_read(
                &tokenizer->mechanics.buffer,
                (void **)&start,
                (void **)&end
            );
            if (line >= end){ return 0; }
        }
    }

    Py_UCS4 c = PyUnicode_READ_CHAR(*line, offset);
    if (is_null){ *is_null = (c == 0); }
    return c;
}

// short form of peek_is_null without null checking
Py_UCS4
peek(WooshTokenizer *tokenizer, size_t offset)
{
    return peek_is_null(tokenizer, offset, 0);
}

// returns the character at the offset within the current span
//
// so 0 is the first character in the span, 1 is the second, etc...
//
// returns 0 if looking beyond the span or a null byte was encountered (so far
// there has been no need to distinguish between the two)
Py_UCS4
review(WooshTokenizer *tokenizer, size_t offset)
{
    assert(tokenizer);
    // find the line that our span starts on, this should always be the first
    // line in the buffer
    PyObject **start;
    PyObject **end;
    fifo_buffer_read(&tokenizer->mechanics.buffer, (void **)&start, (void **)&end);
    assert(tokenizer->mechanics.start.line_index == 0);
    PyObject **line = start;
    if (line >= end){ return 0; }
    // our offset and span may cross lines, so iterate over the lines and adjust
    // our offset until we find the correct one
    offset += tokenizer->mechanics.start.character_index;
    while(1)
    {
        size_t line_length = PyUnicode_GET_LENGTH(*line);
        if (line_length > offset){ break; }
        offset -= line_length;
        line += 1;
        if (line >= end){ return 0; }
    }
    // do not allow reviewing beyond the span
    if (
        line == (start + tokenizer->mechanics.end.line_index) &&
        offset >= tokenizer->mechanics.end.character_index
    ){ return 0; }

    return PyUnicode_READ_CHAR(*line, offset);
}

// like review, but in reverse
//
// the offset is also applied in reverse, so this is like a negative index
// lookup in python, but 0 is like -1, 1 is like -2, etc.
Py_UCS4
review_reverse(WooshTokenizer *tokenizer, size_t offset)
{
    assert(tokenizer);
    // find the line that our span ends with
    PyObject **start;
    PyObject **end;
    fifo_buffer_read(&tokenizer->mechanics.buffer, (void **)&start, (void **)&end);
    PyObject **line = start + tokenizer->mechanics.end.line_index;
    size_t line_length = tokenizer->mechanics.end.character_index;
    // our offset and span may cross lines, so iterate over the lines and adjust
    // our offset until we find the correct one
    offset += 1;
    while(1)
    {
        if (line_length >= offset){ break; }
        offset -= line_length;
        line -= 1;
        if (line < start){ return 0; }
        line_length = PyUnicode_GET_LENGTH(*line);
    }
    offset = line_length - offset;
    if (
        line == (start + tokenizer->mechanics.start.line_index) &&
        offset < tokenizer->mechanics.start.character_index
    )
    {
        return 0;
    }
    return PyUnicode_READ_CHAR(*line, offset);
}

// adds the line to the buffer, stealing the reference
//
// the line must be a unicode object
//
// returns falsey on failure and sets a python exception
int
push(WooshTokenizer *tokenizer, PyObject *line)
{
    assert(tokenizer);
    assert(line);
    assert(PyUnicode_Check(line));
    if (!fifo_buffer_push(
        &tokenizer->mechanics.buffer,
        &line, sizeof(PyObject *)
    ))
    {
        PyErr_NoMemory();
        return 0;
    }
    return 1;
}

// moves the tokenizer span 1 character forward
//
// the combination of characters `\r\n` is treated specially, one call to
// advance will jump over both characters at once
//
// over_null can be specified to control whether the tokenizer will advance over
// a null character or not, typically this is not needed and `advance` is used
// instead
//
// does nothing if the tokenizer is at the end of the source
//
// returns truthy on success and falsey on failure, setting a python exception
int
advance_over_null(WooshTokenizer *tokenizer, int over_null)
{
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && PyErr_Occurred()){ return 0; }
    if (next_c == 0 && review_reverse(tokenizer, 0) == 0 && !over_null)
    {
        return 1;
    }
    // newlines uniquely advance our line position in the file
    if (next_c == '\n')
    {
newline:
        assert(next_c == '\n');
        tokenizer->mechanics.end.line += 1;
        tokenizer->mechanics.end.column = 0;
    }
    else
    {
        tokenizer->mechanics.end.column += 1;
    }
    // every character advances our character index by 1, but that may put us
    // beyond the length of the end line in the buffer, so we need to check
    // that we're not overflowing and if we are then increment to the next
    // line in the buffer
    tokenizer->mechanics.end.character_index += 1;
    PyObject **start;
    PyObject **end;
    fifo_buffer_read(&tokenizer->mechanics.buffer, (void **)&start, (void **)&end);
    PyObject **line = start + tokenizer->mechanics.end.line_index;
    assert(line < end);
    size_t line_length = PyUnicode_GET_LENGTH(*line);
    if (line_length == tokenizer->mechanics.end.character_index)
    {
        tokenizer->mechanics.end.line_index += 1;
        tokenizer->mechanics.end.character_index = 0;
    }
    assert(line_length > tokenizer->mechanics.end.character_index);
    // the \r character is special because if it is followed by a newline then
    // we will also advance over that newline immediatley
    if (next_c == '\r')
    {
        next_c = peek(tokenizer, 0);
        if (next_c == 0 && PyErr_Occurred()){ return 0; }
        if (next_c == '\n'){ goto newline; }
    }
    return 1;
}

// shortcut for advance_over_null without checking the null, typically this
// is what you want
int
advance(WooshTokenizer *tokenizer)
{
    return advance_over_null(tokenizer, 0);
}

// declares that we're done with whatever contents is in the current span,
// making our span empty
void
discard(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->mechanics.start.line_index == 0);
    // we can delete any lines before the end line, since we'll never look at
    // them again
    if (tokenizer->mechanics.end.line_index != 0)
    {
        PyObject **start;
        PyObject **end;
        fifo_buffer_read(
            &tokenizer->mechanics.buffer,
            (void **)&start,
            (void **)&end
        );
        for (size_t i = 0; i < tokenizer->mechanics.end.line_index; i++)
        {
            Py_DECREF(*(start + i));
        }
        fifo_buffer_pop(
            &tokenizer->mechanics.buffer,
            sizeof(PyObject *) * tokenizer->mechanics.end.line_index
        );
        tokenizer->mechanics.end.line_index = 0;
    }
    assert(tokenizer->mechanics.end.line_index == 0);
    tokenizer->mechanics.start = tokenizer->mechanics.end;
}

// exposes the current end column position in the source
size_t
end_column(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    return tokenizer->mechanics.end.column;
}

// exposes the current end line position in the source
size_t
end_line(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    return tokenizer->mechanics.end.line;
}

// indicates that there is no source to read (note that this doesn't mean that
// the buffer is empty, just that all the source has been read into the buffer)
int
at_eof(WooshTokenizer *tokenizer)
{
    assert(tokenizer);
    return tokenizer->mechanics.eof;
}

// create a token of the specified type using the contents of the span
//
// also discards the characters
//
// returns 0 and sets a python exception on failure
WooshToken *
consume(
    WooshTokenizer *tokenizer,
    WooshType* type,
    // 0 to set the value of the token to the contents of the span, otherwise
    // the token will have this object as its contents
    PyObject *value
)
{
    assert(tokenizer);
    assert(type);

    PyObject *start_line = 0;
    PyObject *start_column = 0;
    PyObject *end_line = 0;
    PyObject *end_column = 0;

    if (value)
    {
        // incref so that we can always treat value the same, that is, after
        // this branch we're always holding a reference to it that we will
        // eventually need to decref
        Py_INCREF(value);
    }
    else
    {
        // no value was supplied, so we need to build it from the current span
        PyObject **start;
        PyObject **end;
        fifo_buffer_read(
            &tokenizer->mechanics.buffer,
            (void **)&start,
            (void **)&end
        );
        assert(tokenizer->mechanics.start.line_index == 0);
        // fast path for empty string
        if (start == end)
        {
            value = PyUnicode_FromString("");
            if (!value){ goto error; }
        }
        // fast path for when the token only span one line within the buffer
        else if (tokenizer->mechanics.end.line_index == 0)
        {
            value = PyUnicode_Substring(
                *start,
                tokenizer->mechanics.start.character_index,
                tokenizer->mechanics.end.character_index
            );
            if (!value){ goto error; }
        }
        // fast path for tokens that span a single line within the buffer and
        // end at the very end of it
        else if (
            tokenizer->mechanics.end.line_index == 1 &&
            tokenizer->mechanics.end.character_index == 0
        )
        {
            value = PyUnicode_Substring(
                *start,
                tokenizer->mechanics.start.character_index,
                PyUnicode_GET_LENGTH(*start)
            );
            if (!value){ goto error; }
        }
        // catch-all path for combining multiple lines in the buffer into a
        // single token value
        else
        {
            // we need to determine how large the value will be and create a
            // python unicode object to hold the data
            size_t value_size = 0;
            Py_UCS4 maxchar = 127;
            for (size_t i = 0; i < tokenizer->mechanics.end.line_index; i++)
            {
                PyObject **i_line = start + i;
                value_size += PyUnicode_GET_LENGTH(*i_line);
                Py_UCS4 i_maxchar = PyUnicode_MAX_CHAR_VALUE(*i_line);
                if (i_maxchar > maxchar){ maxchar = i_maxchar; }
            }
            value_size += tokenizer->mechanics.end.character_index;
            value = PyUnicode_New(value_size, maxchar);
            if (!value){ goto error; }
            // copy the first buffer line of characters
            size_t i_position = (
                PyUnicode_GET_LENGTH(*start) -
                tokenizer->mechanics.start.character_index
            );
            if (PyUnicode_CopyCharacters(
                value, 0,
                *start,
                tokenizer->mechanics.start.character_index,
                i_position
            ) == -1){ goto error; }
            // copy the lines in between the start and end
            for (size_t i = 1; i < tokenizer->mechanics.end.line_index; i++)
            {
                PyObject **i_line = start + i;
                size_t line_length = PyUnicode_GET_LENGTH(*i_line);
                if (PyUnicode_CopyCharacters(
                    value, i_position,
                    *i_line, 0, line_length
                ) == -1){ goto error; }
                i_position += line_length;
            }
            // copy the last line of characters
            if (tokenizer->mechanics.end.character_index)
            {
                if (PyUnicode_CopyCharacters(
                    value, i_position,
                    *(end - 1),
                    0,
                    tokenizer->mechanics.end.character_index
                ) == -1){ goto error; }
            }
        }
    }
    // TODO: line creation can be optimized, start and end line is often the
    // same, also many tokens appear on the same line, store the line object on
    // the tokenizer so we're not constantly recreating it
    start_line = PyLong_FromSize_t(tokenizer->mechanics.start.line);
    if (!start_line){ goto error; }
    start_column = PyLong_FromSize_t(tokenizer->mechanics.start.column);
    if (!start_column){ goto error; }
    end_line = PyLong_FromSize_t(tokenizer->mechanics.end.line);
    if (!end_line){ goto error; }
    end_column = PyLong_FromSize_t(tokenizer->mechanics.end.column);
    if (!end_column){ goto error; }
    // we've pulled the values from the span, so we can discard it
    discard(tokenizer);
    // finally create the token, remember that it steals references
    Py_INCREF(type);
    return WooshToken_NEW(
        tokenizer->token,
        type,
        value,
        start_line, start_column,
        end_line, end_column
    );
error:
    Py_CLEAR(value);
    Py_CLEAR(start_line);
    Py_CLEAR(start_column);
    Py_CLEAR(end_line);
    Py_CLEAR(end_column);
    return 0;
}

// shortcut for creating an error token
WooshToken *
error(WooshTokenizer *tokenizer)
{
    return consume(tokenizer, tokenizer->error_type, 0);
}

// shortcut for creating an error token with a specific message, this follows
// the PyUnicode_FromFormat formatting system
WooshToken *
error_format(WooshTokenizer *tokenizer, const char *format, ...)
{
    va_list args;
    va_start(args, format);
    PyObject *message = PyUnicode_FromFormatV(format, args);
    va_end(args);
    if (!message){ return 0; }
    WooshToken *token = consume(tokenizer, tokenizer->error_type, message);
    Py_DECREF(message);
    return token;
}
