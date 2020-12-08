
// this is a very fast python tokenizer/lexer, but it's pretty terrible about
// memory efficiency -- worst case, and most common, scenario it should have
// over 9x the size of the original parsed file in memory:
// - 1x the original source bytes as UTF-8/ASCII
// - 4x the source bytes encoded as what is probably UTF32
// - 4x the source stored for each token as a USC4 unicode python string

// the overall process is pretty simple:
// - bytes are supplied by the caller to be tokenized
// - the encoding for these bytes is determined
// - the bytes are decoded such that each character occupies a distinct word in
//   an array
// - the tokenizer maintains a moving window (the span) which advances across
//   the array
// - at the start of each line any changes to indentation are detected
// - the span is advanced until the end of a token is found
// - the token is created with its type, value and positional information
// - the span collapses to its end point, so that it is empty and the process
//   of advancing repeats
// - after the span reaches the end of the array of characters or if an error
//   occurs, the results are returned the the user

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// stdlib
#include <stdint.h>
// woosh
#include "unicode.h"

// https://en.wikipedia.org/wiki/Byte_order_mark#UTF-8
static const char *UTF8_BOM = "\xEF\xBB\xBF";

// the maximum amount of nested groups (parenthesis, brackets and braces) that
// we'll parse, the CPython tokenizer has the same limitation
#define MAX_GROUPS (200)

// this is the number of spaces to consider a tab for indentation, this is the
// same as CPython
#define TAB_SIZE (8)

// todo: make this not needed
static void *
pointer_add(void *p, size_t offset)
{
    size_t result = 0;
    result = (size_t)((char*)p + offset);
    return (void *)result;
}

// set the key/value of a dict using strings for both
// both the key and value are converted to unicode -- not bytes
//
// returns 0 on failure and sets a python exception
static int
dict_set(PyObject *dict, const char *key, const char *value)
{
    assert(PyDict_Check(dict));
    assert(key);
    assert(value);
    PyObject *p_value = PyUnicode_FromString(value);
    if (!p_value){ return 0; }
    int result = PyDict_SetItemString(dict, key, p_value);
    Py_CLEAR(p_value);
    return result == 0;
}

// per-interpreter module state
struct ModuleState
{
    // contains a re.compile object for checking a line in a python file for the
    // PEP263 encoding comment
    // the ModuleState owns this reference
    PyObject *match_encoding_pattern;
    // quick lookups for the type objects to fill the tokens with
    // the ModuleState does not own these references, they're held implicitly
    // by the module itself (and our ModuleState lifetime is tied to the module)
    PyObject *newline_type;
    PyObject *operator_type;
    PyObject *indent_type;
    PyObject *dedent_type;
    PyObject *name_type;
    PyObject *number_type;
    PyObject *string_type;
    PyObject *comment_type;
    PyObject *eof_type;
    PyObject *error_type;
    PyObject *encoding_type;
};

// describes a position within the tokenizer
struct Position
{
    // note that line starts at 1 and column starts at 0
    size_t line;
    size_t column;
    // a character within the tokenizer source
    Py_UCS4 *slice;
};

// contains the state for the tokenization process
struct Tokenizer
{
    struct ModuleState *module_state;
    // the source we're tokenizing
    Py_UCS4 *source_start;
    Py_UCS4 *source_end;
    // the position of the tokenizer within the source, together the start and
    // end form a span of characters that build the current token
    //
    // note that the end slice is not inclusive, that is, the stop slice
    // indicates the character before which to stop
    struct Position start;
    struct Position end;
    // parenthesis, brackets and braces increment and decrement groups
    //
    // `groups` contains the character which started the group, which will be
    // matched against the closing character, `group_depth` tells us how deep
    // in the stack we are
    //
    // note that the `group_depth` starts at 0 and does not associate with any
    // group in the `groups` stack, `group_depth` 1 is associated with index 0
    // of the `groups`
    //
    // TODO: we might want to allocate this on the heap? this is nearly 1K of
    //      stack memory which will hardly ever even be used -- maybe have a
    //      small stack bucket and a larger heap bucket:
    //      MAX_GROUPS = ...
    //      MAX_GROUPS_STACK = 10;
    //      Py_UCS4 groups[MAX_GROUPS_STACK];
    //      Py_UCS4 *groups2;
    //
    //      such a large array could also effect locality, so it's not only
    //      a concern of eating too much of the stack
    //
    // TODO:
    //       this should also be `unsigned char` instead of Py_UCS4 -- we only
    //       store `(`, '[' and `{` in this array
    //
    //       I suppose this could even be kept as a 2 bit array since we only
    //       store 3 values
    size_t group_depth;
    Py_UCS4 groups[MAX_GROUPS];
    // List[int]
    // a stack describing the indent levels
    // bottom of the stack is always 0
    // top of the stack is the current indentation level
    // TODO:
    //       we're using a python list here because it's easy, but it may be
    //       faster to just use `size_t indents[MAX_INDENTS]` similar to
    //       `groups`
    //
    //       this removes the overhead of having to convert python ints back
    //       and forth -- it's worth noting that the CPython tokenizer also has
    //       a max indents limit that we can copy
    PyObject *indents;
    // the classes to use to generate the tokens
    // the Tokenizer does not own these references, the creator of the Tokenizer
    // must keep them alive for the Tokenizer's lifetime
    //
    // TODO:
    // currently these are supplied by the user, we may be able to increase
    // speed and memory usage by providing c-extension defaults
    //
    // in particular, the position class could be made non-trackable by the GC,
    // since it will only hold refs to integers and is immutable
    //
    // the token class can't be made non-trackable since it is holding enum
    // values which are mutable, but if we also create our own immutable enum
    // values then that could be made GC non-trackable aswell
    PyObject *position_class;
    PyObject *token_class;
    // tells the last type of token that was consumed
    // the Tokenizer does not own this reference, it is implicitly held by the
    // module itself (which the Tokenizer's lifetime is also bound to)
    PyObject *last_token_type;
    // whether the previous line ended with a continuation character
    int is_in_line_continuation;
};

// PEP263 defines a method to describe the encoding of a Python source file
//
// this function may be called one line 1 or 2 to derive the encoding from that
// line if it exists
//
// this function will return None if the line does not exist or if the line does
// not contain an encoding comment
//
// this function will return a Python bytes object containing the name of the
// encoding if there is an encoding comment
static PyObject *
find_encoding_comment(
    struct ModuleState *state,
    const char *source_bytes,
    size_t source_bytes_length,
    size_t line
)
{
    assert(state);
    assert(source_bytes);
    assert(line == 1 || line == 2);
    assert(state->match_encoding_pattern);
    // we need to find the line that we're searching, we currently just have
    // raw bytes, but it should be enough to just search for a newline
    //
    // this isn't a terribly efficient way to find the line we want, but we're
    // only looking at the first two lines and it's pretty simple
    const char *line_start = 0;
    const char *line_end = source_bytes - 1;
    for (size_t i = 0; i < line; i++)
    {
        line_start = line_end + 1;
        line_end = memchr(
            line_start, '\n',
            source_bytes_length - (line_start - source_bytes)
        );
        if (line_end == 0)
        {
            if (i < line - 1)
            {
                Py_RETURN_NONE;
            }
            line_end = source_bytes + source_bytes_length;
            break;
        }
    }
    PyObject *py_line = PyUnicode_FromStringAndSize(
        line_start,
        line_end - line_start
    );
    if (!py_line){ return 0; }

    PyObject *match = PyObject_CallFunction(
        state->match_encoding_pattern, "O",
        py_line
    );
    Py_CLEAR(py_line);
    if (match == 0){ return 0; }
    if (match == Py_None){ return match; }

    PyObject *u_encoding = PyObject_CallMethod(match, "group", "i", 1);
    Py_CLEAR(match);
    if (!u_encoding){ return 0; }
    PyObject *encoding = PyUnicode_AsUTF8String(u_encoding);
    Py_CLEAR(u_encoding);
    return encoding;
}

// PEP-263 defines a method to describe the encoding of a Python source file
//
// this function will determine what encoding is used for the Python source
//
// it will always return a bytes object containing the name to use for decoding
// (ie. "utf-8", "ascii", etc)
static
PyObject *
determine_source_encoding(
    struct ModuleState *state,
    const char *source_bytes,
    size_t source_bytes_length,
    // whether the UTF8 BOM exists in the source
    int utf8_bom
)
{
    assert(state);
    assert(source_bytes);
    // default encoding is utf-8
    PyObject *encoding = PyBytes_FromString("utf-8");
    if (!encoding){ return 0; }
    // only the first two lines may have an encoding comment
    for (size_t i = 1; i < 3; i++)
    {
        PyObject *line_encoding = find_encoding_comment(
            state, source_bytes, source_bytes_length, i
        );
        if (line_encoding == 0){ goto error; }
        if (line_encoding != Py_None)
        {
            Py_CLEAR(encoding);
            encoding = line_encoding;
            break;
        }
        Py_CLEAR(line_encoding);
    }

    const char *encoding_bytes = PyBytes_AsString(encoding);
    if (encoding_bytes == 0){ goto error; }
    // the BOM UTF-8 encoding can't conflict with the encoding comment
    if (
        utf8_bom &&
        strcmp(encoding_bytes, "utf-8") != 0 &&
        strcmp(encoding_bytes, "utf8") != 0
    )
    {
        PyErr_SetString(
            PyExc_ValueError,
            "source has utf-8 BOM, but different encoding comment"
        );
        goto error;
    }
    return encoding;
error:
    Py_CLEAR(encoding);
    return 0;
}

static int
is_whitespace(Py_UCS4 c)
{
    return c == ' ' || c == '\t';
}

// indicates that the character can start a number
static int
is_number_start(Py_UCS4 c)
{
    return '0' <= c && c <= '9';
}

// indicates that the character can be part of the continuation of a number
static int
is_number_continue(Py_UCS4 c)
{
    return is_number_start(c) || c == '_';
}

// indicates that the character can be the binary part of the number following
// the 0b part of the literal
static int
is_binary(Py_UCS4 c)
{
    return '0' == c || c == '1' || c == '_';
}

// indicates that the character can be the octal part of the number following
// the 0o part of the literal
static int
is_octal(Py_UCS4 c)
{
    return ('0' <= c && c <= '7') || c == '_';
}

// indicates that the character can be the hex part of the number following the
// 0x part of the literal
static int
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
static int
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
static int
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

// returns the character after the current tokenizer span at the offset position
//
// typically this would be used with offset of 0 to look at the next character
// that the tokenizer will advance to
//
// returns 0 if looking beyond the end of the source
static Py_UCS4
peek(struct Tokenizer *tokenizer, size_t offset)
{
    assert(tokenizer);
    assert(tokenizer->end.slice);
    assert(tokenizer->source_end);
    // note that the end slice is non-inclusive, so itself is the next peek
    // character at offset 0
    Py_UCS4 *c = (Py_UCS4 *)pointer_add(
        tokenizer->end.slice,
        offset * sizeof(Py_UCS4)
    );
    if (c == 0 || c >= tokenizer->source_end){ return 0; }
    return *c;
}

// returns the character at the offset within the current span, that is 0 is the
// first character in the span, 1 is the second, etc.
//
// returns 0 if looking beyond the span
static Py_UCS4
review(struct Tokenizer *tokenizer, size_t offset)
{
    assert(tokenizer);
    assert(tokenizer->start.slice);
    assert(tokenizer->end.slice);
    Py_UCS4 *c = (Py_UCS4 *)pointer_add(
        tokenizer->start.slice,
        offset * sizeof(Py_UCS4)
    );
    if (c == 0 || c >= tokenizer->end.slice){ return 0; }
    assert(*c != 0);
    return *c;
}

// like review, but in reverse
// the offset is also applied in reverse, so this is like a negative index
// lookup in python, but 0 is like -1, 1 is like -2, etc.
static Py_UCS4
review_reverse(struct Tokenizer *tokenizer, size_t offset)
{
    assert(tokenizer);
    assert(tokenizer->start.slice);
    assert(tokenizer->end.slice);
    // since we're working off of the end slice which is not inclusive, the
    // 0 offset is actually 1, 1 is 2, etc...
    if (offset == SIZE_MAX){ return 0; }
    offset += 1;
    // overflow check
    if (offset > (size_t)tokenizer->end.slice){ return 0; }

    Py_UCS4 *c = tokenizer->end.slice - offset;
    if (c < tokenizer->start.slice){ return 0; }
    assert(*c != 0);
    return *c;
}

// moves the tokenizer 1 character forward
//
// the combination of characters `\r\n` is treated specially, that is one call
// to advance will jump over both characters at once
//
// does nothing if the tokenizer is at the end of the source (however note that
// this will advance over the null byte in the source and add it to the span)
static void
advance(struct Tokenizer *tokenizer)
{
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == 0 && review_reverse(tokenizer, 0) == 0)
    {
        return;
    }
    assert(tokenizer->end.slice < tokenizer->source_end + 1);
    if (next_c == '\n')
    {
        tokenizer->end.slice += 1;
        tokenizer->end.line += 1;
        tokenizer->end.column = 0;
    }
    else if (next_c == '\r' && peek(tokenizer, 1) == '\n')
    {
        tokenizer->end.slice += 2;
        tokenizer->end.line += 1;
        tokenizer->end.column = 0;
    }
    else
    {
        tokenizer->end.slice += 1;
        tokenizer->end.column += 1;
    }
#ifdef DEBUG
    fprintf(stderr, "advance: %u-%u (%u:%u-%u:%u)\n",
        tokenizer->start.slice - tokenizer->source_start,
        tokenizer->end.slice - tokenizer->source_start,
        tokenizer->start.line,
        tokenizer->start.column,
        tokenizer->end.line,
        tokenizer->end.column
    );
#endif
}

// move the start position to the end so that the new span is empty
static void
discard(struct Tokenizer *tokenizer)
{
    tokenizer->start = tokenizer->end;
}

// create a token of the specified type using the contents of the span
//
// also discards the characters
static PyObject *
consume(
    struct Tokenizer *tokenizer,
    PyObject* py_type,
    // 0 to set the value of the token to the contents of the span, otherwise
    // the token will have this object as its contents
    PyObject *py_value
)
{
    assert(tokenizer);
    assert(tokenizer->token_class);
    assert(tokenizer->position_class);
    assert(tokenizer->last_token_type != tokenizer->module_state->error_type);
    assert(py_type);

    PyObject *py_start = 0;
    PyObject *py_end = 0;

    if (py_value)
    {
        // incref so that we can always treat py_value the same, that is, after
        // this branch we're always holding a reference to it that we will
        // eventually need to decref
        Py_INCREF(py_value);
    }
    else
    {
        // TODO:
        //       PyUnicode_FromKindAndData will always create a new string
        //       object (not interned)
        //
        //       for certain token types like OPERATOR, NAME, NEWLINE, INDENT,
        //       DEDENT and possibly STRING we can say that it's probable that
        //       we'll see many of the same value for different tokens
        //
        //       memory usage and (possibly) speed may be improved by interning
        //       these types
        //
        //       further, while the tokenizer might slow a bit, whatever is
        //       parsing the tokens may benefit from interned strings, as there
        //       is a fast path for the == operator on unicode objects that are
        //       the same -- this probably only applies to OPERATOR tokens, as
        //       those would often be compared by value and not type
        //
        //       STRING requires some extra consideration, small strings are
        //       often repeated (dict keys for example), but large strings are
        //       usually unique within a codebase (docstrings), so some cutoff
        //       in length may need to be used to determine whether the STRING
        //       value is to be interned
        py_value = PyUnicode_FromKindAndData(
            PyUnicode_4BYTE_KIND,
            tokenizer->start.slice,
            tokenizer->end.slice - tokenizer->start.slice
        );
        if (!py_value){ goto error; }
    }

    // TODO:
    //       it would not be terribly uncommon for the start of this token to be
    //       the same as the end of the previous token -- it may be worth
    //       storing that information and re-using the previous token's start
    //       position
    //
    //       presumably this would reduce memory usage and may give us some
    //       speed up
    py_start = PyObject_CallFunction(
        tokenizer->position_class,
        "II",
        tokenizer->start.line,
        tokenizer->start.column
    );
    if (!py_start){ goto error; }

    py_end = PyObject_CallFunction(
        tokenizer->position_class,
        "II",
        tokenizer->end.line,
        tokenizer->end.column
    );
    if (!py_end){ goto error; }

    discard(tokenizer);

    PyObject *token = PyObject_CallFunction(
        tokenizer->token_class, "OOOO", // 🐟
        py_type, py_value, py_start, py_end
    );
    // tokenizer does not hold a reference here, it is implicitly held by the
    // module
    tokenizer->last_token_type = py_type;

    Py_CLEAR(py_value);
    Py_CLEAR(py_start);
    Py_CLEAR(py_end);
    return token;
error:
    Py_CLEAR(py_value);
    Py_CLEAR(py_start);
    Py_CLEAR(py_end);
    return 0;
}

static PyObject *
error(struct Tokenizer *tokenizer)
{
    return consume(tokenizer, tokenizer->module_state->error_type, 0);
}

static PyObject *
number(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    return consume(tokenizer, tokenizer->module_state->number_type, 0);
}

static PyObject *
operator(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    return consume(tokenizer, tokenizer->module_state->operator_type, 0);
}

// this function determines whether to emit indent and dedent tokens, unlike
// most parse_ functions it does not return a token object, it returns a list
// of token objects or None
//
// this function must only be called at the start of a line with span of 0
//
// TODO: potential speed increase
//       the return  list gets generated here new each time, maybe have one list
//       stored on the tokenizer, clear it, fill with data and return int to
//       tell caller to copy tokens from it?
//
//       this *could* also allow for a generator based API
static PyObject *
parse_line_start(struct Tokenizer *tokenizer)
{
    assert(tokenizer);
    assert(tokenizer->module_state);
    assert(tokenizer->module_state->indent_type);
    assert(tokenizer->module_state->dedent_type);
    assert(tokenizer->start.line == tokenizer->end.line);
    assert(tokenizer->start.column == 0);
    assert(tokenizer->end.column == 0);
    assert(tokenizer->indents);
    assert(!tokenizer->is_in_line_continuation);
    assert(PyList_Check(tokenizer->indents));

    PyObject *results = 0;
    PyObject *indents = 0;

    results = Py_None;
    Py_INCREF(results);
    // note that PySequence_Fast increfs
    indents = PySequence_Fast(
        tokenizer->indents,
        "tokenizer indents is not a fast sequence"
    );
    if (!indents){ goto error; }

    Py_UCS4 next_c = peek(tokenizer, 0);
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
        advance(tokenizer);
        next_c = peek(tokenizer, 0);
    }
#ifdef DEBUG
    fprintf(stderr, "line indent is: %u\n", line_indent);
#endif
    // if we're currently in a group (parenthesis, brackets, braces)
    // then indentation cannot change
    if (tokenizer->group_depth)
    {
        discard(tokenizer);
        Py_CLEAR(indents);
        return results;
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
        advance(tokenizer);
        discard(tokenizer);
        Py_CLEAR(indents);
        return results;
    }
    // we need to compare the indent of this line to the current indentation
    // level, so that we can see if it has changed
    size_t current_indent;
    {
        // note that PySequence_Fast_GET_ITEM returns a borrowed ref, no
        // need to decref
        PyObject* py_current_indent = PySequence_Fast_GET_ITEM(
            indents,
            PySequence_Fast_GET_SIZE(indents) - 1
        );
        if (!py_current_indent){ goto error; }
        assert(PyLong_Check(py_current_indent));
        current_indent = PyLong_AsSize_t(py_current_indent);
        if (PyErr_Occurred()){ goto error; }
    }
#ifdef DEBUG
    fprintf(stderr, "current indent is %u\n", current_indent);
#endif
    // if we've indented then we'll emit an INDENT token
    if (current_indent < line_indent)
    {
        // the new indent goes on the top of the indent stack so that we can
        // track it
        {
            PyObject *py_line_indent = PyLong_FromLong(line_indent);
            if (!py_line_indent){ goto error; }
            int append = PyList_Append(indents, py_line_indent);
            Py_CLEAR(py_line_indent);
            if (append != 0){ goto error; }
        }
        {
            PyObject *token = consume(
                tokenizer,
                tokenizer->module_state->indent_type,
                0
            );
            if (!token){ goto error; }
            Py_CLEAR(results);
            results = PyList_New(1);
            if (!results)
            {
                Py_CLEAR(token);
                goto error;
            }
            PyList_SET_ITEM(results, 0, token);
        }
    }
    // if we've dedented then we'll need to emit some number of DEDENT
    // tokens or an error if the new indentation level is not in the stack
    else if (current_indent > line_indent)
    {
        // we need to find the new indentation level in the stack, that will
        // let us know how many DEDENTS to emit
        //
        // for example if our current stack is `[0, 4, 8, 12]`
        // and the new indentation level is `4`
        // then we'll emit two DEDENT tokens to account for the loss of
        // indentation levels `8` and `12`
        size_t indents_length = PyList_GET_SIZE(indents);
        assert(indents_length);
        PyObject **indents_items = PySequence_Fast_ITEMS(indents);
        assert(indents_items);
        size_t i;
        for(i = 0; i < indents_length; i++)
        {
            PyObject *py_indent = indents_items[i];
            size_t indent = PyLong_AsSize_t(py_indent);
            if (PyErr_Occurred()){ goto error; }
            if (indent == line_indent){ break; }
        }
        // if the indentation level was not found in the stack then it is
        // an error
        //
        // for example if the stack is `[0, 4, 8, 12]` and the new
        // indentation level is `6` then it is an error -- the author did
        // not dedent to an existing block
        if (i == indents_length)
        {
            PyObject *token = error(tokenizer);
            if (!token){ goto error; }
            Py_DECREF(results);
            results = PyList_New(1);
            if (!results)
            {
                Py_CLEAR(token);
                goto error;
            }
            PyList_SET_ITEM(results, 0, token);
        }
        // here the indentation was found in the stack, so we'll emit those
        // DEDENT tokens
        else
        {
            // here we're just converting i to 1 based indexing instead of
            // 0, this makes more sense for all the operations we'll perform
            // in this section (slicing and length based stuff)
            i += 1;
            // we can get rid of the extra indents from the stack
            {
                PyObject *new_indents = PyList_GetSlice(indents, 0, i);
                if (!new_indents){ goto error; }
                Py_CLEAR(indents);
                indents = new_indents;
            }
            // and then create a DEDENT for each indent removed
            Py_DECREF(results);
            results = PyList_New(indents_length - i);
            if (!results){ goto error; }
            // TODO:
            //       there is a possibly insignificant optimization that could
            //       be made here
            //
            //       any DEDENT token generated after the 1st will always be
            //       the same (value-wise) as the 2nd token generated
            //       this is because the 1st DEDENT consumes whatever is in the
            //       tokenizer span and the rest are just empty
            //
            //       so, rather than running consume on each token after the
            //       2nd we can simply copy the 2nd token however many remaining
            //       times
            //
            //       I can't imagine this being a significant improvement
            //       however
            //
            //       It's worth noting that the tokenizer module doesn't have
            //       values for dedents, so may we can just spit out copies of
            //       the first one with no value in all cases -- this might
            //       actually yield some super minor gain
            size_t oi;
            for(oi = 0; oi < indents_length - i; oi++)
            {
                PyObject* token = consume(
                    tokenizer,
                    tokenizer->module_state->dedent_type,
                    0
                );
                if (!token){ goto error; }
                PyList_SET_ITEM(results, oi, token);
            }
        }
    }
    // the indent level might be (and often is) the same, so there is
    // nothing then to do
    else
    {
        discard(tokenizer);
    }

    Py_DECREF(tokenizer->indents);
    tokenizer->indents = indents;
    return results;
error:
    Py_CLEAR(indents);
    Py_CLEAR(results);
    return 0;
}

// parse a newline character
//
// the span must either be `\n` or `\r\n`
static PyObject *
parse_newline(struct Tokenizer *tokenizer)
{
    assert(
        (review(tokenizer, 0) == '\n' && review(tokenizer, 1) == 0) ||
        (
            review(tokenizer, 0) == '\r' &&
            review(tokenizer, 1) == '\n' &&
            review(tokenizer, 2) == 0
        )
    );
    tokenizer->is_in_line_continuation = 0;
    // we only emit a NEWLINE token when we're not currently in a group (that
    // is within parenthesis, brackets or braces)
    if (tokenizer->group_depth == 0)
    {
        return consume(tokenizer, tokenizer->module_state->newline_type, 0);
    }
    discard(tokenizer);
    Py_RETURN_NONE;
}

// parse whitespace
//
// the span must be 1 and the only character in the span must be whitespace
static PyObject *
parse_whitespace(struct Tokenizer *tokenizer)
{
    assert(is_whitespace(review(tokenizer, 0)));
    assert(review(tokenizer, 1) == 0);
    // discard all the whitespace that comes after the initial whitespace
    // character
    while(is_whitespace(peek(tokenizer, 0))){ advance(tokenizer); }
    discard(tokenizer);
    Py_RETURN_NONE;
}

// parse a number from the exponent part
//
// the last character in the buffer must be `e` or `E`
static PyObject *
parse_exponent(struct Tokenizer *tokenizer)
{
    Py_UCS4 start_c = review_reverse(tokenizer, 0);
    assert(start_c == 'e' || start_c == 'E');
    // the exponent part may optionally be followed by a `+` or `-`
    Py_UCS4 next_c = peek(tokenizer, 0);
    switch(next_c)
    {
        case '+':
        case '-':
            advance(tokenizer);
            break;
        default:
            break;
    }
    // after the `+` or `-` comes numbers, but the first one may not be a `_`
    if (peek(tokenizer, 0) == '_')
    {
        advance(tokenizer);
        return error(tokenizer);
    }
    // the optional `+` or `-` must be followed by a number
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (!is_number_continue(next_c)){ break; }
        advance(tokenizer);
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        last_c = next_c;
    }
    // the exponent part must end with an actual 0-9 number
    if (last_c == '_' || !is_number_continue(last_c))
    {
        if (peek(tokenizer, 0))
        {
            advance(tokenizer);
        }
        return error(tokenizer);
    }
    // the exponent numbers may optionally be followed by `j` or `J` to denote
    // imaginary-ness
    next_c = peek(tokenizer, 0);
    switch(next_c)
    {
        case 'j':
        case 'J':
            advance(tokenizer);
            break;
        default:
            break;
    }
    return number(tokenizer);
}

// parse something that is a float
//
// the last character in the span must be `.`
static PyObject *
parse_float(struct Tokenizer *tokenizer)
{
    assert(review_reverse(tokenizer, 0) == '.');
    // after the `.` comes numbers, but the first one may not be a `_`
    if (peek(tokenizer, 0) == '_')
    {
        advance(tokenizer);
        return error(tokenizer);
    }
    // a set of numbers or underscores *may* follow the `.` (0. is acceptable
    // for example)
    Py_UCS4 last_c = review_reverse(tokenizer, 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (!is_number_continue(next_c)){ break; }
        // two underscores may not follow each other
        advance(tokenizer);
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        last_c = next_c;
    }
    // the last character in the numbers section may not be an `_`
    if (last_c == '_')
    {
        return error(tokenizer);
    }
    // the number may be followed by an exponent or imaginary component
    Py_UCS4 next_c = peek(tokenizer, 0);
    switch(next_c)
    {
        case 'e':
        case 'E':
            advance(tokenizer);
            return parse_exponent(tokenizer);
        case 'j':
        case 'J':
            advance(tokenizer);
            break;
        default:
            break;
    }
    return number(tokenizer);
}

// parse something starting with a '.'
//
// the span must be 1 and the only character in the span must be a `.`
static PyObject *
parse_dot(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '.');
    assert(review(tokenizer, 1) == 0);

    Py_UCS4 next_c = peek(tokenizer, 0);
    // the ellipsis (...) will always be composed of three consecutive dots
    if (next_c == '.' && peek(tokenizer, 1) == '.')
    {
        advance(tokenizer);
        advance(tokenizer);
    }
    // a dot that is followed by a number (0-9) is a float
    else if (is_number_start(next_c))
    {
        return parse_float(tokenizer);
    }
    // `.` or `...`
    return operator(tokenizer);
}

// parse something starting with a `-`
//
// the span must be 1 and the only character in the span must be a `-`
static PyObject *
parse_minus(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '-');
    assert(review(tokenizer, 1) == 0);
    // `-` is either `-` `->` or `-=`
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == '>' || next_c == '=')
    {
        advance(tokenizer);
    }
    return operator(tokenizer);
}

// parse an operator that may be followed by an `=`
//
// for example the character `+` may be either `+` or `+=`
// also the set of characters `**` may be either `**` or `**=`
//
// the span must be atleast 1
static PyObject *
parse_operator_equal_follows(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) != 0);
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == '=')
    {
        advance(tokenizer);
    }
    return operator(tokenizer);
}

// parse an operator that may be followed by itself, itself and an `=` or just
// and '='
//
// for example the character `*` may be either `*`, `**`, `*=`, or `**=`
//
// the span must be 1 and the only character
static PyObject *
parse_operator_double_equal_follows(struct Tokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c != 0);
    assert(review(tokenizer, 1) == 0);
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c == start_c){ advance(tokenizer); }
    return parse_operator_equal_follows(tokenizer);
}

// parse something start with `!`
//
// the span must be 1 and the only character in the span must be a `!`
static PyObject *
parse_bang(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '!');
    assert(review(tokenizer, 1) == 0);
    // the `!` character must be immediatley followed by a `=` character to make
    // the `!=` operator token
    Py_UCS4 next_c = peek(tokenizer, 0);
    if (next_c != '=')
    {
        return error(tokenizer);
    }
    advance(tokenizer);
    return operator(tokenizer);
}

// parse an operator which starts a group
//
// the span must be 1 and the only character in the span must be a `(`, `[` or
// `{`
static PyObject *
parse_open_operator(struct Tokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c == '(' || start_c == '[' || start_c == '{');
    assert(review(tokenizer, 1) == 0);
    if (tokenizer->group_depth == MAX_GROUPS)
    {
        return error(tokenizer);
    }
    tokenizer->groups[tokenizer->group_depth] = start_c;
    tokenizer->group_depth += 1;
    return operator(tokenizer);
}

// parse an operator which ends a group
//
// the span must be 1 and the only character in the span must be a `)`, `]` or
// `}`
static PyObject *
parse_close_operator(struct Tokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert(start_c == ')' || start_c == ']' || start_c == '}');
    assert(review(tokenizer, 1) == 0);
    // a close token when there is no open token is unexpected
    if (tokenizer->group_depth == 0)
    {
        return error(tokenizer);
    }
    // a close token that doesn't match the current open token is unexpected
    Py_UCS4 open_c = tokenizer->groups[tokenizer->group_depth - 1];
    Py_UCS4 match_c = 0;
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
            break;
    }
    if (start_c != match_c)
    {
        return error(tokenizer);
    }

    tokenizer->group_depth -= 1;
    return operator(tokenizer);
}

// parse an `\` character, which causes a line continuation
//
// the span must be 1 and the only character in the span must be a `\`
//
// note that this is unlike most parse functions as it may return None instead
// of a token object
static PyObject *
parse_continuation(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '\\');
    assert(review(tokenizer, 1) == 0);
    // we don't want to tokenize the continuation character itself
    discard(tokenizer);
    // strip everything after the continuation character, there should only be
    // whitespace between the continuation character and the newline
    int token_error = 0;
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (
            next_c == 0 ||
            next_c == '\n' ||
            (next_c == '\r' && peek(tokenizer, 1) == '\n')
        )
        {
            break;
        }
        if (!is_whitespace(next_c)){ token_error = 1; }
        advance(tokenizer);
    }
    PyObject *error_token = 0;
    if (token_error)
    {
        error_token = error(tokenizer);
    }
    tokenizer->is_in_line_continuation = 1;
    // strip out the newline
    advance(tokenizer);
    discard(tokenizer);
    // we may need to return an error token
    if (error_token){ return error_token; }
    Py_RETURN_NONE;
}

// parse a `#` character and the remaining line as a comment
//
// the span must be 1 and the only character in the span must be a `#`
static PyObject *
parse_comment(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '#');
    assert(review(tokenizer, 1) == 0);
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (
            next_c == '\n' ||
            (next_c == '\r' && peek(tokenizer, 1) == '\n') ||
            next_c == 0
        )
        {
            break;
        }
        advance(tokenizer);
    }
    return consume(tokenizer, tokenizer->module_state->comment_type, 0);
}

// parse a binary integer literal
//
// the span must be 2 and the characters must be either `0b` or `0B`
static PyObject *
parse_binint(struct Tokenizer *tokenizer)
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
        if (!is_binary(next_c)){ break; }
        advance(tokenizer);
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        last_c = next_c;
    }
    if (last_c == '_' || !is_binary(last_c))
    {
        if (peek(tokenizer, 0))
        {
            advance(tokenizer);
        }
        return error(tokenizer);
    }
    // note that binary integer literals may not have an exponent or imaginary
    // component
    return number(tokenizer);
}

// parse an octal integer literal
//
// the span must be 2 and the characters must be either `0o` or `0O`
static PyObject *
parse_octint(struct Tokenizer *tokenizer)
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
        if (!is_octal(next_c)){ break; }
        advance(tokenizer);
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        last_c = next_c;
    }
    if (last_c == '_' || !is_octal(last_c))
    {
        if (peek(tokenizer, 0))
        {
            advance(tokenizer);
        }
        return error(tokenizer);
    }
    // note that octal integer literals may not have an exponent or imaginary
    // component
    return number(tokenizer);
}

// parse a hex integer literal
//
// the span must be 2 and the characters must be either `0x` or `0X`
PyObject *
parse_hexint(struct Tokenizer *tokenizer)
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
        if (!is_hex(next_c)){ break; }
        advance(tokenizer);
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            return error(tokenizer);
        }
        last_c = next_c;
    }
    if (last_c == '_' || !is_hex(last_c))
    {
        if (peek(tokenizer, 0))
        {
            advance(tokenizer);
        }
        return error(tokenizer);
    }
    return number(tokenizer);
}

// parse something that starts with 0
//
// the span must be 1 and the character must be `0`
static PyObject *
parse_zero(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == '0');
    assert(review(tokenizer, 1) == 0);
    for(size_t i = 0; ; i++)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        switch(next_c)
        {
            // note that for any of the non-decimal types it must be that there
            // is only one zero in the literal, otherwise it's an error
            // ex: `00x0` is not valid
            case 'b':
            case 'B':
                advance(tokenizer);
                if (i){ return error(tokenizer); }
                return parse_binint(tokenizer);
            case 'o':
            case 'O':
                advance(tokenizer);
                if (i){ return error(tokenizer); }
                return parse_octint(tokenizer);
            case 'x':
            case 'X':
                advance(tokenizer);
                if (i){ return error(tokenizer); }
                return parse_hexint(tokenizer);
            case 'e':
            case 'E':
                advance(tokenizer);
                return parse_exponent(tokenizer);
            case 'j':
            case 'J':
                advance(tokenizer);
                return number(tokenizer);
            case '.':
                advance(tokenizer);
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
                advance(tokenizer);
                return error(tokenizer);
            // zero may be followed by other zeroes, just continue looping
            case '0':
                advance(tokenizer);
                break;
            // zero may be followed by an underscore (and another zero), again
            // continue looping
            case '_':
                advance(tokenizer);
                next_c = peek(tokenizer, 0);
                if (next_c != '0')
                {
                    // this advance is to make error reporting consistent with
                    // the non-zero case where a double underscore is consumed
                    // by the error
                    if (next_c == '_'){ advance(tokenizer); }
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
static PyObject *
parse_number(struct Tokenizer *tokenizer)
{
    Py_UCS4 start_c = review(tokenizer, 0);
    assert('1' <= start_c && start_c <= '9');
    assert(review(tokenizer, 1) == 0);
    // the first number may be followed by more numbers
    Py_UCS4 last_c = start_c;
    while(1)
    {
        Py_UCS4 next_c = peek(tokenizer, 0);
        if (!is_number_continue(next_c)){ break; }
        // two underscores may not follow each other
        if (last_c == '_' && next_c == '_')
        {
            advance(tokenizer);
            return error(tokenizer);
        }
        advance(tokenizer);
        last_c = next_c;
    }
    // the number may not end with an underscore or a non-number
    if (last_c == '_')
    {
        return error(tokenizer);
    }
    // the number may be followed by a `.`, exponent or imaginary sigil
    Py_UCS4 next_c = peek(tokenizer, 0);
    switch(next_c)
    {
        case '.':
            advance(tokenizer);
            return parse_float(tokenizer);
        case 'e':
        case 'E':
            advance(tokenizer);
            return parse_exponent(tokenizer);
        case 'j':
        case 'J':
            advance(tokenizer);
            break;
        default:
            break;
    }
    return number(tokenizer);
}

// parse a string (which can either be a byte string or a unicode string)
//
// the span must be atleast 1 with the last character being a quote
static PyObject *
parse_string(
    struct Tokenizer *tokenizer,
    int is_bytes // 1 if this is a bytes string (otherwise a unicode string)
)
{
    Py_UCS4 quote = review_reverse(tokenizer, 0);
    assert(quote == '\'' || quote == '"');
    // determine the number of quote characters, this should be either 1 or 3
    size_t quote_count = 1;
    for (size_t i = 0; i < 2; i++)
    {
        if (peek(tokenizer, quote_count - 1) == quote)
        {
            quote_count += 1;
        }
        else
        {
            break;
        }
    }
    // it's possible that we have an empty single quoted string, which would be
    // detected as a quote count of 2
    if (quote_count == 2){ quote_count = 1; }
    // remember -- we already have the first quote in the span, so we only need
    // to advance over additional quotes
    for (size_t i = 1; i < quote_count; i++)
    {
        advance(tokenizer);
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
                return error(tokenizer);
            }
            // bytes string literals may only contain ASCII characters
            else if (is_bytes && next_c >= 128)
            {
                advance(tokenizer);
                return error(tokenizer);
            }

            if (!escape)
            {
                if (next_c == quote){ break; }
                // only triple quote strings can span multiple lines
                if (next_c == '\\'){ escape = 1; }
                else if (
                    quote_count == 1 &&
                    (
                        next_c == '\n' ||
                        (next_c == '\r' && peek(tokenizer, 1) == '\n')
                    )
                )
                {
                    advance(tokenizer);
                    return error(tokenizer);
                }
            }
            else
            { escape = 0; }

            advance(tokenizer);
        }
        // we've found the end quote character, but for triple quotes that isn't
        // necessarily the end, we need to make sure its 3 quotes in a row
        // if not, then we restart this loop and search again
        assert(peek(tokenizer, 0) == quote);
        advance(tokenizer);
        size_t i;
        for (i = 1; i < quote_count; i++)
        {
            if (peek(tokenizer, 0) != quote){ break; }
            advance(tokenizer);
        }
        if (i == quote_count){ break; }
    }
    return consume(tokenizer, tokenizer->module_state->string_type, 0);
}

// parse something that is a name/identifier
//
// the start character must be a character that a name may start with
// the remaining characters in the span must be characters that a name may
// continue with
static PyObject *
parse_name(struct Tokenizer *tokenizer)
{
    assert(is_name_start(review(tokenizer, 0)));
    for(size_t i = 1;; i++)
    {
        Py_UCS4 continue_c = review(tokenizer, i);
        if (continue_c == 0){ break; }
        assert(is_name_continue(continue_c));
    }

    while(is_name_continue(peek(tokenizer, 0))){ advance(tokenizer); }

    return consume(tokenizer, tokenizer->module_state->name_type, 0);
}

// parse something that might be a unicode string or a name/identifier
//
// the span must be at least 1 or 2 characters
// if 1 character, it must be either 'f', 'F', 'u' or 'U'
// if 2 characters, it must be some combination of 'f' and 'r' with any mixing
// of cases
static PyObject *
parse_unicode_or_name(struct Tokenizer *tokenizer)
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
    // if our buffer just has `f` we have a unique path because it may be
    // followed by `r` and still be a unicode string
    if (
        c_1 == 0 &&
        (c_0 == 'f' || c_0 == 'F') &&
        (next_c == 'r' || next_c == 'R')
    )
    {
        advance(tokenizer);
        c_1 = next_c;
        next_c = peek(tokenizer, 0);
    }
    switch(next_c)
    {
        case '\'':
        case '"':
            advance(tokenizer);
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
static PyObject *
parse_bytes_or_name(struct Tokenizer *tokenizer)
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
    if (
        c_1 == 0 &&
        (c_0 == 'b' || c_0 == 'B') &&
        (next_c == 'r' || next_c == 'R')
    )
    {
        advance(tokenizer);
        c_1 = next_c;
        next_c = peek(tokenizer, 0);
    }
    switch(next_c)
    {
        case '\'':
        case '"':
            advance(tokenizer);
            return parse_string(tokenizer, 1);
        default:
            return parse_name(tokenizer);
    }
}

// parse something that might be a unicode string, bytes string or a
// name/identifier
//
// the span must be at 1 character, either 'r' or 'R'
static PyObject *
parse_unicode_bytes_or_name(struct Tokenizer *tokenizer)
{
    assert(review(tokenizer, 0) == 'r' || review(tokenizer, 0) == 'R');
    assert(review(tokenizer, 1) == 0);

    Py_UCS4 next_c = peek(tokenizer, 0);
    switch(next_c)
    {
        case 'f':
        case 'F':
            advance(tokenizer);
            return parse_unicode_or_name(tokenizer);
        case 'b':
        case 'B':
            advance(tokenizer);
            return parse_bytes_or_name(tokenizer);
        case '\'':
        case '"':
            advance(tokenizer);
            return parse_string(tokenizer, 0);
        default:
            return parse_name(tokenizer);
    }
}

// parse the next token, assuming that the tokenization logic for a line start
// has already been done (parse_line_start)
//
// the span must contain exactly 1 character or the character combination `\r\n`
static PyObject *
parse(struct Tokenizer *tokenizer)
{
    // null bytes within the source are a bit weird because the review functions
    // treat the source like there isn't null bytes in it (which is usually
    // true)
    //
    // no token accepts a null byte, so we can rely on this parse function to
    // eject us from a malformed source
    assert(tokenizer->start.slice);
    assert(tokenizer->end.slice);
    if (tokenizer->start.slice == tokenizer->end.slice)
    {
        assert(*tokenizer->start.slice == 0);
        assert(tokenizer->end.slice < tokenizer->source_end);
        tokenizer->end.slice += 1;
        tokenizer->end.column += 1;
        return error(tokenizer);
    }

    assert(
        (review(tokenizer, 0) != 0 && review(tokenizer, 1) == 0) ||
        (
            review(tokenizer, 0) =='\r' &&
            review(tokenizer, 1) == '\n' &&
            review(tokenizer, 2) == 0
        )
    );

    Py_UCS4 start_c = review(tokenizer, 0);
#ifdef DEBUG
    fprintf(stderr, "parsing: '%c'\n", start_c);
#endif
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
        case '<':
        case '>':
            return parse_operator_double_equal_follows(tokenizer);
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

static PyObject *
tokenize_impl(
    struct ModuleState *module_state,
    PyObject *source,
    const char *encoding,
    PyObject *token_class,
    PyObject *position_class
)
{
    assert(module_state);
    assert(source);
    assert(token_class);
    assert(PyUnicode_Check(source));

    size_t source_length = PyUnicode_GET_LENGTH(source);
    Py_UCS4 *u_source = 0;
    struct Tokenizer tokenizer = {0};
    PyObject *results = 0;

    u_source = PyUnicode_AsUCS4Copy(source);
    if (!u_source){ goto error; }

    tokenizer.module_state = module_state;
    tokenizer.source_start = u_source;
    tokenizer.source_end = u_source + source_length;
    tokenizer.start.line = 1;
    tokenizer.start.slice = u_source;
    tokenizer.end.line = 1;
    tokenizer.end.slice = u_source;
    tokenizer.indents = PyList_New(0);
    tokenizer.position_class = position_class;
    tokenizer.token_class = token_class;
    if (tokenizer.indents == 0){ goto error; }
    // the indents stack will always have at least one number in it: 0
    // this simplifies the algorithms later so we don't have to do any special
    // cases for no indentation
    {
        PyObject* zero = PyLong_FromLong(0);
        if (!zero){ goto error; }
        int append = PyList_Append(tokenizer.indents, zero);
        Py_CLEAR(zero);
        if (append != 0){ goto error; }
    }

    // always include an ENCODING token as the first token
    results = PyList_New(1);
    if (!results){ goto error; }
    {
        PyObject *py_encoding = PyUnicode_FromString(encoding);
        if (!py_encoding){ goto error; }
        PyObject *encoding_token = consume(
            &tokenizer,
            tokenizer.module_state->encoding_type,
            py_encoding
        );
        Py_CLEAR(py_encoding);
        if (!encoding_token){ goto error; }
        PyList_SET_ITEM(results, 0, encoding_token);
    }
    // now we can parse until we encounter an error or reach the end of the file
    while(
        tokenizer.last_token_type != module_state->error_type &&
        tokenizer.end.slice < tokenizer.source_end
    )
    {
        if (tokenizer.end.column == 0 && !tokenizer.is_in_line_continuation)
        {
            size_t line = tokenizer.end.line;
#ifdef DEBUG
            fprintf(stderr, "parsing start of line %u\n", line);
#endif
            PyObject *tokens = parse_line_start(&tokenizer);
            if (!tokens){ goto error; }
            if (tokens != Py_None)
            {
                assert(PySequence_Check(tokens));
                PyObject* py_temp = PySequence_InPlaceConcat(results, tokens);
                Py_CLEAR(tokens);
                if (!py_temp){ goto error; }
                assert(py_temp == results);
                Py_CLEAR(py_temp);
                continue;
            }
            Py_CLEAR(tokens);
            if (line != tokenizer.end.line){ continue; }
        }

        advance(&tokenizer);
        PyObject *token = parse(&tokenizer);
        if (!token){ goto error; }
        if (token != Py_None)
        {
            int append = PyList_Append(results, token);
            Py_CLEAR(token);
            if (append != 0){ goto error; }
        }
        else
        {
            Py_CLEAR(token);
        }
    }
    // do some house cleaning if we've not encountered an error
    if (tokenizer.last_token_type != module_state->error_type)
    {
        // if the last token is not a newline, add a newline
        if (tokenizer.last_token_type != module_state->newline_type)
        {
            PyObject *token = consume(&tokenizer, module_state->newline_type, 0);
            if (!token){ goto error; }
            int append = PyList_Append(results, token);
            Py_CLEAR(token);
            if (append != 0){ goto error; }
        }
        // dedent back to 0
        size_t indent_count = PyList_GET_SIZE(tokenizer.indents);
        for (size_t i = 1; i < indent_count; i++)
        {
            PyObject *token = consume(&tokenizer, module_state->dedent_type, 0);
            if (!token){ goto error; }
            int append = PyList_Append(results, token);
            Py_CLEAR(token);
            if (append != 0){ goto error; }
        }
        // end with an EOF token
        {
            PyObject *token = consume(&tokenizer, module_state->eof_type, 0);
            if (!token){ goto error; }
            int append = PyList_Append(results, token);
            Py_CLEAR(token);
            if (append != 0){ goto error; }
        }
    }

    Py_CLEAR(tokenizer.indents);
    PyMem_Free(u_source);
    return results;
error:
    Py_CLEAR(results);
    Py_CLEAR(tokenizer.indents);
    PyMem_Free(u_source);
    return 0;
}

static PyObject *
tokenize(PyObject *self, PyObject *args)
{
    struct ModuleState *module_state = PyModule_GetState(self);
    assert(module_state);

    PyObject *source_bytes;
    PyObject *token_class;
    PyObject *position_class;
    if (!PyArg_ParseTuple(
            args, "SOO",
            &source_bytes,
            &token_class,
            &position_class
    )){ return 0; };
    Py_INCREF(source_bytes);
    // detect and eliminate the utf-8 bom from the source (if there is one)
    //
    // this makes it so the rest of the code doesn't have to worry about the
    // BOM intefering with parsing
    int utf8_bom = (
        PyBytes_GET_SIZE(source_bytes) >= strlen(UTF8_BOM) &&
        memcmp(PyBytes_AS_STRING(source_bytes), UTF8_BOM, strlen(UTF8_BOM)) == 0
    );
    if (utf8_bom)
    {
        PyObject *source_bytes_no_utf8_bom = PySequence_GetSlice(
            source_bytes,
            strlen(UTF8_BOM),
            PyBytes_GET_SIZE(source_bytes)
        );
        Py_CLEAR(source_bytes);
        if (!source_bytes_no_utf8_bom){ goto error; }
        source_bytes = source_bytes_no_utf8_bom;
    }

    PyObject *encoding = determine_source_encoding(
        module_state,
        PyBytes_AS_STRING(source_bytes),
        PyBytes_GET_SIZE(source_bytes),
        utf8_bom
    );
    if (!encoding){ goto error; }
    assert(PyBytes_Check(encoding));

    PyObject *source = PyUnicode_FromEncodedObject(
        source_bytes,
        PyBytes_AS_STRING(encoding),
        0
    );
    if (!source)
    {
        if (PyErr_ExceptionMatches(PyExc_LookupError))
        {
            PyErr_Clear();
            PyObject *error_message = PyUnicode_FromFormat(
                "invalid encoding: %R", encoding
            );
            if (error_message)
            {
                PyErr_SetObject(PyExc_ValueError, error_message);
                Py_CLEAR(error_message);
            }
        }
        Py_CLEAR(encoding);
        goto error;
    }

    PyObject* result = tokenize_impl(
        module_state,
        source,
        PyBytes_AS_STRING(encoding),
        token_class,
        position_class
    );
    Py_CLEAR(source_bytes);
    Py_CLEAR(source);
    Py_CLEAR(encoding);
    return result;
error:
    Py_CLEAR(source_bytes);
    return 0;
}

static PyMethodDef methods[] = {
    {"tokenize",  tokenize, METH_VARARGS, "docstring"},
    {NULL, NULL, 0, NULL}
};

static int
traverse(PyObject *self, visitproc visit, void *arg)
{
#ifdef DEBUG
    fprintf(stderr, "visit\n");
#endif
    struct ModuleState *module_state = PyModule_GetState(self);
    assert(module_state);
    Py_VISIT(module_state->match_encoding_pattern);
    return 0;
}

static int
clear(PyObject *self)
{
#ifdef DEBUG
    fprintf(stderr, "clear\n");
#endif
    struct ModuleState *module_state = PyModule_GetState(self);
    assert(module_state);
    Py_CLEAR(module_state->match_encoding_pattern);
    return 0;
}

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "token",
    0,
    sizeof(struct ModuleState),
    methods,
    0,
    traverse,
    clear
};

PyMODINIT_FUNC
PyInit__tokenizer()
{
    PyObject *module = PyModule_Create(&module_def);
    if (!module){ return 0; }

    struct ModuleState *state = PyModule_GetState(module);
    assert(state);
    {
        PyObject *re = PyImport_ImportModule("re");
        if (!re){ goto error; }

        PyObject *encoding_pattern = PyObject_CallMethod(
            re, "compile", "s",
            "^[ \\t\\f]*#.*?coding[:=][ \\t]*([-_.a-zA-Z0-9]+)"
        );
        Py_CLEAR(re);
        if (!encoding_pattern){ goto error; }

        PyObject *match_encoding_pattern = PyObject_GetAttrString(
            encoding_pattern, "match"
        );
        Py_CLEAR(encoding_pattern);
        if (!match_encoding_pattern){ goto error; }
        // state steals match_encoding_pattern ref
        state->match_encoding_pattern = match_encoding_pattern;
        match_encoding_pattern = 0;
    }

    // token types are an enum which we'll attach to the module itself, however
    // the module state will have direct references to the actual enum values
    // for quick lookup
    //
    // we make the assumption here that the enum will maintain our refs to these
    // values, as we aren't doing it ourselves
    {
        PyObject *token_types = PyDict_New();
        if (!token_types){ goto error; }
        if (
            !dict_set(token_types, "NEWLINE", "L") ||
            !dict_set(token_types, "OPERATOR", "O") ||
            !dict_set(token_types, "INDENT", "I") ||
            !dict_set(token_types, "DEDENT", "D") ||
            !dict_set(token_types, "NAME", "A") ||
            !dict_set(token_types, "NUMBER", "U") ||
            !dict_set(token_types, "STRING", "S") ||
            !dict_set(token_types, "COMMENT", "C") ||
            !dict_set(token_types, "EOF", "E") ||
            !dict_set(token_types, "ERROR", "X") ||
            !dict_set(token_types, "ENCODING", "N")
        )
        {
            Py_CLEAR(token_types);
            goto error;
        }

        PyObject *enum_ = PyImport_ImportModule("enum");
        if (!enum_)
        {
            Py_CLEAR(token_types);
            goto error;
        }

        PyObject *token_type = PyObject_CallMethod(
            enum_, "Enum", "sO",
            "TokenType", token_types
        );
        Py_CLEAR(enum_);
        if (!token_type){ return 0; }
        state->newline_type = PyObject_GetAttrString(token_type, "NEWLINE");
        assert(state->newline_type);
        state->operator_type = PyObject_GetAttrString(token_type, "OPERATOR");
        assert(state->operator_type);
        state->indent_type = PyObject_GetAttrString(token_type, "INDENT");
        assert(state->indent_type);
        state->dedent_type = PyObject_GetAttrString(token_type, "DEDENT");
        assert(state->dedent_type);
        state->name_type = PyObject_GetAttrString(token_type, "NAME");
        assert(state->name_type);
        state->number_type = PyObject_GetAttrString(token_type, "NUMBER");
        assert(state->number_type);
        state->string_type = PyObject_GetAttrString(token_type, "STRING");
        assert(state->string_type);
        state->comment_type = PyObject_GetAttrString(token_type, "COMMENT");
        assert(state->comment_type);
        state->eof_type = PyObject_GetAttrString(token_type, "EOF");
        assert(state->eof_type);
        state->error_type = PyObject_GetAttrString(token_type, "ERROR");
        assert(state->error_type);
        state->encoding_type = PyObject_GetAttrString(token_type, "ENCODING");
        assert(state->encoding_type);
        // PyModule_AddObject steals reference to token_type on success
        int add_object = PyModule_AddObject(module, "TokenType", token_type);
        Py_CLEAR(token_types);
        if (add_object < 0)
        {
            Py_CLEAR(token_type);
            goto error;
        }
    }

    return module;
error:
    Py_CLEAR(state->match_encoding_pattern);
    Py_CLEAR(module);
    return 0;
}
