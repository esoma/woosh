
// This file contains the definition for the Tokenizer extension type. Most of
// its guts are implemented in different sub-files. The Tokenizer acts as a
// generator, spitting out Tokens for a given source input.

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// woosh
#include "lifobuffer.h"
#include "modulestate.h"
#include "woosh/tokenobject.h"
#include "woosh/tokenizerobject.h"
#include "tokenizerobject_internal.h"

static WooshTokenizer *create_tokenizer(PyObject *, PyObject *);
static WooshToken *iter_tokenizer(WooshTokenizer *);

// tp_dealloc for Tokenizer
static void
woosh_tokenizer_dealloc(WooshTokenizer *self)
{
    if (self->weakreflist)
    {
        PyObject_ClearWeakRefs((PyObject *)self);
    }
    
    Py_CLEAR(self->type);
    Py_CLEAR(self->token);
    Py_CLEAR(self->newline_type);
    Py_CLEAR(self->operator_type);
    Py_CLEAR(self->indent_type);
    Py_CLEAR(self->dedent_type);
    Py_CLEAR(self->name_type);
    Py_CLEAR(self->number_type);
    Py_CLEAR(self->string_type);
    Py_CLEAR(self->comment_type);
    Py_CLEAR(self->eof_type);
    Py_CLEAR(self->error_type);
    Py_CLEAR(self->encoding_type);
    Py_CLEAR(self->source);

    dealloc_mechanics(self);
    dealloc_parse(self);
    dealloc_encoding(self);
    dealloc_groups(self);
    dealloc_indent(self);
    
    PyTypeObject *type = Py_TYPE(self);
    type->tp_free(self);
    Py_DECREF(type);
}

// tp_iter for Tokenizer
static WooshTokenizer *
woosh_tokenizer_iter(WooshTokenizer *self)
{
    Py_INCREF(self);
    return self;
}

// tp_iternext for Tokenizer
static PyObject *
woosh_tokenizer_iternext(WooshTokenizer *self)
{
    return (PyObject *)WooshTokenizer_NEXT(self);
}

static PyMemberDef woosh_tokenizer_type_members[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof(WooshTokenizer, weakreflist), READONLY},
    {0}
};

static PyType_Slot woosh_tokenizer_spec_slots[] = {
    {Py_tp_dealloc, (destructor)woosh_tokenizer_dealloc},
    {Py_tp_iter, (getiterfunc)woosh_tokenizer_iter},
    {Py_tp_iternext, (iternextfunc)woosh_tokenizer_iternext},
    {Py_tp_members, woosh_tokenizer_type_members},
    {0, 0},
};

static PyType_Spec woosh_tokenizer_spec = {
    "woosh.Tokenizer",
    sizeof(WooshTokenizer),
    0,
    Py_TPFLAGS_DEFAULT,
    woosh_tokenizer_spec_slots
};

// initializes the type extension class
// returns a new reference
PyTypeObject *
WooshTokenizer_Initialize_(PyObject *module)
{
#if PY_VERSION_HEX >= 0x03090000
    PyTypeObject *type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &woosh_tokenizer_spec,
        0
    );
#else
    PyTypeObject* type = (PyTypeObject *)PyType_FromSpec(&woosh_tokenizer_spec);
#endif
    return type;
}

// create a Tokenizer instance
WooshTokenizer *
WooshTokenizer_New_(PyObject *module, PyObject *source)
{
    assert(module);
    assert(source);
    return create_tokenizer(module, source);
}

// get the Tokenizer type
PyTypeObject *
WooshTokenizer_Get_()
{
    struct WooshModuleState *state = WooshModuleState_Get_();
    if (!state){ return 0; }
    assert(state->tokenizer);
    return state->tokenizer;
}

// check that the object is a Tokenizer or subtype of Tokenizer
int
WooshTokenizer_Check(PyObject *self)
{
    return PyType_IsSubtype(Py_TYPE(self), WooshTokenizer_Get_());
}

// check that the object is exactly a Tokenizer
int
WooshTokenizer_CheckExact(PyObject * self)
{
    return Py_TYPE(self) == WooshTokenizer_Get_();
}

// get the next Token from the Tokenizer
// may return 0 with a python error set, raises StopIteration when finished
// tokenizing
PyObject *
WooshTokenizer_Next(PyObject * self)
{
    if (WooshTokenizer_Check(self))
    {
        return (PyObject *)WooshTokenizer_NEXT((WooshTokenizer *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Tokenizer");
}

// get the next Token from the Tokenizer without error checking on the input
WooshToken *
WooshTokenizer_NEXT(WooshTokenizer *self)
{
    assert(WooshTokenizer_Check((PyObject *)self));
    return iter_tokenizer(self);
}

// internal initializer for the Tokenizer
static WooshTokenizer *
create_tokenizer(PyObject *module, PyObject *source)
{
    struct WooshModuleState *module_state = PyModule_GetState(module);
    assert(module_state);

    WooshTokenizer *tokenizer = (WooshTokenizer *)PyType_GenericAlloc(
        module_state->tokenizer,
        0
    );
    if (!tokenizer){ return 0; }

#define COPY_MODULE_STATE(name)\
    Py_INCREF(module_state->name);\
    tokenizer->name = module_state->name;

    COPY_MODULE_STATE(type);
    COPY_MODULE_STATE(token);
    COPY_MODULE_STATE(newline_type);
    COPY_MODULE_STATE(operator_type);
    COPY_MODULE_STATE(indent_type);
    COPY_MODULE_STATE(dedent_type);
    COPY_MODULE_STATE(name_type);
    COPY_MODULE_STATE(number_type);
    COPY_MODULE_STATE(string_type);
    COPY_MODULE_STATE(comment_type);
    COPY_MODULE_STATE(eof_type);
    COPY_MODULE_STATE(error_type);
    COPY_MODULE_STATE(encoding_type);
#undef COPY_MODULE_STATE

    Py_INCREF(source);
    tokenizer->source = source;

    if (!init_mechanics(tokenizer)){ goto error; }
    if (!init_parse(tokenizer)){ goto error; }
    if (!init_encoding(tokenizer)){ goto error; }
    if (!init_groups(tokenizer)){ goto error; }
    if (!init_indent(tokenizer)){ goto error; }

    return tokenizer;
error:
    Py_DECREF(tokenizer);
    return 0;
}

// internal iterator for the Tokenizer
static WooshToken *
iter_tokenizer(WooshTokenizer *tokenizer)
{
    WooshToken *token = parse(tokenizer);
    if (!token)
    {
        if (!PyErr_Occurred())
        {
            PyErr_SetString(PyExc_StopIteration, "");
        }
        return 0;
    }
    return token;
}
