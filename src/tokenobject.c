
// This file describes the Token python extension type which is the main output
// of the tokenize function. Each Token object has a type which describes a
// category in which the Token falls under, the value which is a string object
// describing the characters the form the token, and a start/end line/column
// which describe the physical position of the token value within the source.
// Tokens are immutable.

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// woosh
#include "modulestate.h"
#include "woosh/tokenobject.h"

struct WooshToken_
{
    PyObject_HEAD
    PyObject *weakreflist;
    WooshType *type;
    PyObject *value;
    PyObject* start_line;
    PyObject* start_column;
    PyObject* end_line;
    PyObject* end_column;
};

// tp_new for Token
static PyObject *
woosh_token_new(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"", "", "", "", "", "", NULL};
    PyObject *type;
    PyObject *value;
    PyObject *start_line;
    PyObject *start_column;
    PyObject *end_line;
    PyObject *end_column;
    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "OOOOOO|", kwlist,
        &type, &value, &start_line, &start_column, &end_line, &end_column
    )){ return 0; } // LCOV_EXCL_LINE

    return WooshToken_New(
        type, value,
        start_line, start_column,
        end_line, end_column
    );
}

// tp_dealloc for Token
static void
woosh_token_dealloc(WooshToken *self)
{
    if (self->weakreflist)
    {
        PyObject_ClearWeakRefs((PyObject *)self);
    }
    
    Py_CLEAR(self->type);
    Py_CLEAR(self->value);
    Py_CLEAR(self->start_line);
    Py_CLEAR(self->start_column);
    Py_CLEAR(self->end_line);
    Py_CLEAR(self->end_column);
    
    PyTypeObject *type = Py_TYPE(self);
    type->tp_free(self);
    Py_DECREF(type);
}

// tp_getattro for Token
static PyObject *
woosh_token_getattro(WooshToken *self, PyObject *py_attr)
{
    const char *attr = PyUnicode_AsUTF8(py_attr);
    if (!attr){ return 0; }

    if (strcmp(attr, "type") == 0)
    {
        Py_INCREF(self->type);
        return (PyObject *)self->type;
    }
    else if (strcmp(attr, "value") == 0)
    {
        Py_INCREF(self->value);
        return (PyObject *)self->value;
    }
    else if (strcmp(attr, "start_line") == 0)
    {
        Py_INCREF(self->start_line);
        return (PyObject *)self->start_line;
    }
    else if (strcmp(attr, "start_column") == 0)
    {
        Py_INCREF(self->start_column);
        return (PyObject *)self->start_column;
    }
    else if (strcmp(attr, "end_line") == 0)
    {
        Py_INCREF(self->end_line);
        return (PyObject *)self->end_line;
    }
    else if (strcmp(attr, "end_column") == 0)
    {
        Py_INCREF(self->end_column);
        return (PyObject *)self->end_column;
    }

    return PyObject_GenericGetAttr((PyObject *)self, py_attr);
}

// tp_richcompare for Token
static PyObject *
woosh_token_richcompare(WooshToken *self, PyObject *unk_other, int op)
{
    if (WooshToken_Check(unk_other) && (op == Py_EQ || op == Py_NE))
    {
        WooshToken *other = (WooshToken*)unk_other;
        int cmp = (
            PyObject_RichCompareBool((PyObject *)self->type, (PyObject *)other->type, Py_EQ) &&
            PyUnicode_Compare(self->value, other->value) == 0 &&
            PyObject_RichCompareBool(self->start_line, other->start_line, Py_EQ) &&
            PyObject_RichCompareBool(self->start_column, other->start_column, Py_EQ) &&
            PyObject_RichCompareBool(self->end_line, other->end_line, Py_EQ) &&
            PyObject_RichCompareBool(self->end_column, other->end_column, Py_EQ)
        );
        if (op == Py_NE){ cmp = !cmp; }

        if (cmp){ Py_RETURN_TRUE; }
        else { Py_RETURN_FALSE; }
    }
    Py_RETURN_NOTIMPLEMENTED;
}

// tp_repr for Token
static PyObject *
woosh_token_repr(WooshToken *self)
{
    return PyUnicode_FromFormat(
        "<Token %R %R %R:%R-%R:%R>",
        self->type, self->value,
        self->start_line, self->start_column,
        self->end_line, self->end_column
    );
}

static PyMemberDef woosh_token_type_members[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof(WooshToken, weakreflist), READONLY},
    {0}
};

static PyType_Slot woosh_token_spec_slots[] = {
    {Py_tp_new, woosh_token_new},
    {Py_tp_dealloc, (destructor)woosh_token_dealloc},
    {Py_tp_getattro, (getattrofunc)woosh_token_getattro},
    {Py_tp_richcompare, (getattrfunc)woosh_token_richcompare},
    {Py_tp_repr, (getattrfunc)woosh_token_repr},
    {Py_tp_members, woosh_token_type_members},
    {0, 0},
};

static PyType_Spec woosh_token_spec = {
    "woosh.Token",
    sizeof(WooshToken),
    0,
    Py_TPFLAGS_DEFAULT,
    woosh_token_spec_slots
};

// initialize the Token extension type for the module adding it to the module
// as "Token"
//
// returns the extension type on success or 0 and sets a python error on failure
PyTypeObject *
WooshToken_Initialize_(PyObject *module)
{
#if PY_VERSION_HEX >= 0x03090000
    PyTypeObject *type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &woosh_token_spec,
        0
    );
#else
    PyTypeObject* type = (PyTypeObject *)PyType_FromSpec(&woosh_token_spec);
    // hack for 3.6-8 to support weakrefs
    type->tp_weaklistoffset = offsetof(WooshToken, weakreflist);
#endif
    // Note:
    // Unlike other functions that steal references, PyModule_AddObject() only
    // decrements the reference count of value on success.
    if (PyModule_AddObject(module, "Token", (PyObject *)type) < 0)
    {
        // LCOV_EXCL_START
        Py_DECREF(type);
        return 0;
        // LCOV_EXCL_STOP
    }
    return type;
}

// get the Token extension type
PyTypeObject *
WooshToken_Get()
{
    struct WooshModuleState *state = WooshModuleState_Get_();
    if (!state){ return 0; }
    assert(state->token);
    return state->token;
}

// check that the object is a Token or a subtype of Token
int
WooshToken_Check(PyObject *self)
{
    return PyType_IsSubtype(Py_TYPE(self), WooshToken_Get());
}

// check that the object is a Token exactly
int
WooshToken_CheckExact(PyObject *self)
{
    return Py_TYPE(self) == WooshToken_Get();
}

// create a new Token object
PyObject *
WooshToken_New(
    PyObject *type, PyObject *value,
    PyObject *start_line, PyObject *start_column,
    PyObject *end_line, PyObject *end_column
)
{
    if (!WooshType_CheckExact(type))
    {
        return PyErr_Format(PyExc_TypeError, "type must be woosh.Type");
    }
    if (!PyUnicode_CheckExact(value))
    {
        return PyErr_Format(PyExc_TypeError, "value must be str");
    }
    if (!PyLong_CheckExact(start_line))
    {
        return PyErr_Format(PyExc_TypeError, "start_line must be int");
    }
    if (!PyLong_CheckExact(start_column))
    {
        return PyErr_Format(PyExc_TypeError, "start_column must be int");
    }
    if (!PyLong_CheckExact(end_line))
    {
        return PyErr_Format(PyExc_TypeError, "end_line must be int");
    }
    if (!PyLong_CheckExact(end_column))
    {
        return PyErr_Format(PyExc_TypeError, "end_column must be int");
    }

    Py_INCREF(type);
    Py_INCREF(value);
    Py_INCREF(start_line);
    Py_INCREF(start_column);
    Py_INCREF(end_line);
    Py_INCREF(end_column);

    return (PyObject *)WooshToken_NEW(
        WooshToken_Get(),
        (WooshType *)type, value,
        start_line, start_column,
        end_line, end_column
    );
}

// create a new token object without error checking on inputs
//
// py_type should be the Token type
//
// this function steals a reference to type, value, start_line, start_column,
// end_line and end_column
WooshToken *
WooshToken_NEW(
    PyTypeObject *py_type,
    WooshType *type, PyObject *value,
    PyObject *start_line, PyObject *start_column,
    PyObject *end_line, PyObject *end_column
)
{
    assert(PyType_Check(py_type));
    assert(WooshType_Check((PyObject *)type));
    assert(PyUnicode_CheckExact(value));
    assert(PyLong_CheckExact(start_line));
    assert(PyLong_CheckExact(start_column));
    assert(PyLong_CheckExact(end_line));
    assert(PyLong_CheckExact(end_column));

    WooshToken *self = (WooshToken *)PyType_GenericAlloc(py_type, 0);
    if (!self)
    {
        // LCOV_EXCL_START
        Py_DECREF(type);
        Py_DECREF(value);
        Py_DECREF(start_line);
        Py_DECREF(start_column);
        Py_DECREF(end_line);
        Py_DECREF(end_column);
        return 0;
        // LCOV_EXCL_STOP
    }

    self->type = type;
    self->value = value;
    self->start_line = start_line;
    self->start_column = start_column;
    self->end_line = end_line;
    self->end_column = end_column;

    return self;
}

// gets the Type for the Token
PyObject *
WooshToken_GetType(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_TYPE((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// gets the Type for the Token without error checking
WooshType *
WooshToken_GET_TYPE(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->type;
}

// gets the value of the Token
PyObject *
WooshToken_GetValue(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_VALUE((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// gets the value of the Token without error checking
PyObject *
WooshToken_GET_VALUE(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->value;
}

// gets the start line of the Token
PyObject *
WooshToken_GetStartLine(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_START_LINE((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// gets the start line of the Token without error checking
PyObject *
WooshToken_GET_START_LINE(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->start_line;
}

// gets the start column of the Token
PyObject *
WooshToken_GetStartColumn(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_START_COLUMN((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// gets the start column of the Token without error checking
PyObject *
WooshToken_GET_START_COLUMN(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->start_column;
}

// gets the end line of the Token
PyObject *
WooshToken_GetEndLine(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_END_LINE((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// gets the end line of the Token without error checking
PyObject *
WooshToken_GET_END_LINE(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->end_line;
}

// get the end column of the Token
PyObject *
WooshToken_GetEndColumn(PyObject *self)
{
    if (WooshToken_Check(self))
    {
        return (PyObject *)WooshToken_GET_END_COLUMN((WooshToken *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Token");
}

// get the end column of the Token without error checking
PyObject *
WooshToken_GET_END_COLUMN(WooshToken *self)
{
    assert(WooshToken_Check((PyObject *)self));
    return self->end_column;
}
