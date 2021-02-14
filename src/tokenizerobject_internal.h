
// this is an internal header which exposes the guts of the tokenizer object
//
// the actual implementation of the functions are split across several files and
// are logically grouped by their purpose

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "fifobuffer.h"
#include "lifobuffer.h"

// describes both a position within the file (line and column) and position
// within the internal buffer (line_index, character index)
struct Position
{
    // note that line starts at 1 and column starts at 0
    size_t line;
    size_t column;
    // the index of the python unicode object in the buffer
    size_t line_index;
    // the index of the character in the python unicode object
    size_t character_index;
};

// state for the "mechanics" of the tokenizer object
//
// mechanics mostly has to do with how the tokenizer reads the source and
// provides an interface for the rest of the internals to access it
struct Mechanics
{
    // buffer of python unicode objects read from source
    // the strings at the front of the buffer are removed as they are processed
    // and strings are appended to the end of the buffer as they are needed
    FifoBuffer buffer;
    // the position of the tokenizer within the source, together the start and
    // end form a span of characters that build the current token
    //
    // note that the end slice is not inclusive, that is, the stop slice
    // indicates the character before which to stop
    struct Position start;
    struct Position end;
    // whether the end of the source has been reached
    int eof;
};

// state for the "parse" portion of the tokenizer object
//
// "parse" mostly has to do with overall/general parsing state or things which
// are not complicated enough to warrant their own submodule
struct Parse
{
    // whether the previous line ended with a continuation character
    int is_in_line_continuation;
    // tells the last type of token that was consumed
    // the Tokenizer does not own this reference, it is implicitly held by the
    // module itself (which the Tokenizer's lifetime is also bound to)
    WooshType *last_token_type;
    // whether the required newline prior to the eof has been emitted
    int eof_newline;
    // whether the end marker token has been emitted
    int endmarker;
};

// state for the "encoding" porition of the tokenizer object
//
// "encoding" strictly deals with discovering the encoding of the source, but
// it does bleed into the mechanics a bit as mechanics depends on knowing the
// encoding before it can really work
struct Encoding
{
    // bytes string of the detected encoding for the source
    // may be 0 if encoding hasn't been detected yet
    PyObject *name;
};

// state for the "groups" portion of the tokenizer object
//
// "groups" deals with knowledge of grouping characters within the source (that
// is parenthesis, brackets and braces)
struct Groups
{
    // stack of current opening group characters: (, [, {
    // these are stored as a char
    LifoBuffer stack;
};

// state for the "indent" portion of the tokenizer object
//
// "indent" deals with detecting and tracking indentation levels
struct Indent
{
    // stack of the current indentation levels as a size_t
    LifoBuffer stack;
    // the number of dedents pending to be emitted
    size_t dedents_pending;
};

// the tokenizer object itself combines all these different submodules
struct WooshTokenizer_
{
    PyObject_HEAD
    PyObject *weakreflist;
    
    // extension types defined on the module
    PyTypeObject *type;
    PyTypeObject *token;
    // all the type instances defined on the module
    WooshType *newline_type;
    WooshType *nl_type;
    WooshType *operator_type;
    WooshType *indent_type;
    WooshType *dedent_type;
    WooshType *name_type;
    WooshType *number_type;
    WooshType *string_type;
    WooshType *comment_type;
    WooshType *eof_type;
    WooshType *error_type;
    WooshType *encoding_type;

    PyObject *source;

    struct Mechanics mechanics;
    struct Parse parse;
    struct Encoding encoding;
    struct Groups groups;
    struct Indent indent;
};

// tokenizerobject_parse.c
int init_parse(WooshTokenizer *);
void dealloc_parse(WooshTokenizer *);
int visit_parse(WooshTokenizer *, visitproc, void *);
int clear_parse(WooshTokenizer *);
WooshToken *parse(WooshTokenizer *);
WooshToken *parse_name(WooshTokenizer *);
// tokenizerobject_encode.c
int init_encoding(WooshTokenizer *);
void dealloc_encoding(WooshTokenizer *);
int visit_encoding(WooshTokenizer *, visitproc, void *);
int clear_encoding(WooshTokenizer *);
const char *encoding(WooshTokenizer *);
WooshToken *parse_encoding(WooshTokenizer *);
// tokenizerobject_indent.c
int init_indent(WooshTokenizer *);
void dealloc_indent(WooshTokenizer *);
int visit_indent(WooshTokenizer *, visitproc, void *);
int clear_indent(WooshTokenizer *);
WooshToken *parse_line_start(WooshTokenizer *);
WooshToken *continue_dedent(WooshTokenizer *);
WooshToken *cleanup_dedents(WooshTokenizer *);
// tokenizerobject_sets.c
int is_whitespace(Py_UCS4);
int is_number_start(Py_UCS4);
int is_number_continue(Py_UCS4);
int is_binary(Py_UCS4);
int is_octal(Py_UCS4);
int is_hex(Py_UCS4);
int is_name_start(Py_UCS4);
int is_name_continue(Py_UCS4);
// tokenizerobject_mechanics.c
int init_mechanics(WooshTokenizer *);
void dealloc_mechanics(WooshTokenizer *);
int visit_mechanics(WooshTokenizer *, visitproc, void *);
int clear_mechanics(WooshTokenizer *);
Py_UCS4 peek_is_null(WooshTokenizer *, size_t, int *);
Py_UCS4 peek(WooshTokenizer *, size_t);
Py_UCS4 review(WooshTokenizer *, size_t);
Py_UCS4 review_reverse(WooshTokenizer *, size_t);
int push(WooshTokenizer *, PyObject *);
int advance(WooshTokenizer *);
int advance_over_null(WooshTokenizer *, int);
void discard(WooshTokenizer *);
size_t end_column(WooshTokenizer *);
size_t end_line(WooshTokenizer *);
int at_eof(WooshTokenizer *);
WooshToken *consume(WooshTokenizer *, WooshType*, PyObject *);
WooshToken *error(WooshTokenizer *);
WooshToken *error_format(WooshTokenizer *, const char *, ...);
// tokenizerobject_groups.c
int init_groups(WooshTokenizer *);
void dealloc_groups(WooshTokenizer *);
int visit_groups(WooshTokenizer *, visitproc, void *);
int clear_groups(WooshTokenizer *);
char peek_group(WooshTokenizer *);
WooshToken *parse_open_operator(WooshTokenizer *);
WooshToken *parse_close_operator(WooshTokenizer *);
// tokenizerobject_operator.c
WooshToken *operator(WooshTokenizer *);
WooshToken *parse_dot(WooshTokenizer *);
WooshToken *parse_operator_equal_follows(WooshTokenizer *);
WooshToken *parse_operator_double_equal_follows(WooshTokenizer *);
WooshToken *parse_less_than(WooshTokenizer *);
WooshToken *parse_minus(WooshTokenizer *);
WooshToken *parse_bang(WooshTokenizer *);
// tokenizerobject_string.c
WooshToken *parse_unicode_bytes_or_name(WooshTokenizer *);
WooshToken *parse_bytes_or_name(WooshTokenizer *);
WooshToken *parse_unicode_or_name(WooshTokenizer *);
WooshToken *parse_string(WooshTokenizer *, int);
// tokenizerobject_number.c
WooshToken *parse_float(WooshTokenizer *);
WooshToken *parse_zero(WooshTokenizer *);
WooshToken *parse_number(WooshTokenizer *);
