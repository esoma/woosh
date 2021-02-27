
// This file describes the Type python extension type. Types are categories of
// Tokens (operators, strings, names, etc). Types are similar in purpose and
// function to python's Enum, but are immutable. Each type has a name, which is
// human-readable and value which is some unique number between 0 and 255.

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// woosh
#include "modulestate.h"
#include "woosh/typeobject.h"

struct WooshType_
{
    PyObject_HEAD
    PyObject *weakreflist;
    PyObject *name;
    unsigned char raw_value;
    PyObject *value;
};

// tp_new for Type
static PyObject *
woosh_type_new(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"", "", NULL};
    PyObject *name;
    PyObject *value;
    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "OO|", kwlist,
        &name, &value
    )){ return 0; }

    return WooshType_New(name, value);
}

// tp_dealloc for Type
static void
woosh_type_dealloc(WooshType *self)
{
    if (self->weakreflist)
    {
        PyObject_ClearWeakRefs((PyObject *)self);
    }
    
    Py_CLEAR(self->name);
    Py_CLEAR(self->value);
    
    PyTypeObject *type = Py_TYPE(self);
    type->tp_free(self);
    Py_DECREF(type);
}

// tp_getattro for Type
static PyObject *
woosh_type_getattro(WooshType *self, PyObject *py_attr)
{
    const char *attr = PyUnicode_AsUTF8(py_attr);
    if (!attr){ return 0; }

    if (strcmp(attr, "name") == 0)
    {
        Py_INCREF(self->name);
        return (PyObject *)self->name;
    }
    else if (strcmp(attr, "value") == 0)
    {
        Py_INCREF(self->value);
        return (PyObject *)self->value;
    }

    return PyObject_GenericGetAttr((PyObject *)self, py_attr);
}

// tp_richcompare for Type
static PyObject *
woosh_type_richcompare(WooshType *self, PyObject *unk_other, int op)
{
    if (PyUnicode_Check(unk_other))
    {
        return PyObject_RichCompare((PyObject *)self->value, unk_other, op);
    }
    else if (WooshType_Check(unk_other) && (op == Py_EQ || op == Py_NE))
    {
        WooshType *other = (WooshType*)unk_other;
        int cmp = self->raw_value == other->raw_value;
        if (op == Py_NE){ cmp = !cmp; }

        if (cmp){ Py_RETURN_TRUE; }
        else { Py_RETURN_FALSE; }
    }
    Py_RETURN_NOTIMPLEMENTED;
}

// tp_repr for Type
static PyObject *
woosh_type_repr(WooshType *self)
{
    Py_INCREF(self->name);
    return(PyObject *)self->name;
}

static PyMemberDef woosh_type_type_members[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof(WooshType, weakreflist), READONLY},
    {0}
};

static PyType_Slot woosh_type_spec_slots[] = {
    {Py_tp_new, woosh_type_new},
    {Py_tp_dealloc, (destructor)woosh_type_dealloc},
    {Py_tp_getattro, (getattrofunc)woosh_type_getattro},
    {Py_tp_richcompare, (getattrfunc)woosh_type_richcompare},
    {Py_tp_repr, (getattrfunc)woosh_type_repr},
    {Py_tp_members, woosh_type_type_members},
    {0, 0},
};

static PyType_Spec woosh_type_spec = {
    "woosh.Type",
    sizeof(WooshType),
    0,
    Py_TPFLAGS_DEFAULT,
    woosh_type_spec_slots
};

// initialize the Type extension type for the module adding it to the module
// as "Type"
//
// returns the extension type on success or 0 and sets a python error on failure
PyTypeObject *
WooshType_Initialize_(PyObject *module)
{
#if PY_VERSION_HEX >= 0x03090000
    PyTypeObject *type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &woosh_type_spec,
        0
    );
#else
    PyTypeObject* type = (PyTypeObject *)PyType_FromSpec(&woosh_type_spec);
    // hack for 3.6-8 to support weakrefs
    type->tp_weaklistoffset = offsetof(WooshType, weakreflist);
#endif
    // Note:
    // Unlike other functions that steal references, PyModule_AddObject() only
    // decrements the reference count of value on success.
    if (PyModule_AddObject(module, "Type", (PyObject *)type) < 0)
    {
        // LCOV_EXCL_START
        Py_DECREF(type);
        return 0;
        // LCOV_EXCL_STOP
    }
    return type;
}

// convenience function for adding a new Type instance to a module
//
// a call like this:
//    WooshType_Add_(module, "EXAMPLE", 1)
// would be equivalent to
//    EXAMPLE = woosh.Type('EXAMPLE', 1)
// in python
//
// returns a borrowed reference of the created type
WooshType *
WooshType_Add_(PyObject *module, const char* raw_name, unsigned char raw_value)
{
    PyObject *name = PyUnicode_FromString(raw_name);
    if (!name){ return 0; }

    struct WooshModuleState * state = (
        (struct WooshModuleState *)PyModule_GetState(module)
    );
    PyTypeObject *type = state->type;
    assert(type);

    // note: WooshType_NEW steals reference to name
    WooshType *self = WooshType_NEW(type, name, raw_value);
    if (!self){ return 0; }

    if (PyModule_AddObject(module, raw_name, (PyObject *)self) < 0)
    {
        // LCOV_EXCL_START
        Py_DECREF(self);
        return 0;
        // LCOV_EXCL_STOP
    }

    return self;
}

// get the Type extension type
PyTypeObject *
WooshType_Get()
{
    struct WooshModuleState *state = WooshModuleState_Get_();
    if (!state){ return 0; }
    assert(state->type);
    return state->type;
}

// check that the object is a Type or a subtype of Type
int
WooshType_Check(PyObject *self)
{
    return PyType_IsSubtype(Py_TYPE(self), WooshType_Get());
}

// check that the object is a Type exactly
int
WooshType_CheckExact(PyObject *self)
{
    return Py_TYPE(self) == WooshType_Get();
}

// create a new Type object
PyObject *
WooshType_New(PyObject *name, PyObject *value)
{
    if (!PyUnicode_CheckExact(name))
    {
        return PyErr_Format(PyExc_TypeError, "name must be str");
    }
    if (!PyLong_CheckExact(value))
    {
        return PyErr_Format(PyExc_TypeError, "value must be int");
    }
    long raw_value = PyLong_AsLong(value);
    if (raw_value == -1 && PyErr_Occurred()){ return 0; }
    if (raw_value < 0 || raw_value > 255)
    {
        return PyErr_Format(PyExc_ValueError, "value must be between 0 and 255");
    }

    PyTypeObject* type = WooshType_Get();
    if (!type){ return 0; }

    WooshType *self = (WooshType *)PyType_GenericAlloc(type, 0);
    if (!self){ return 0; }

    Py_INCREF(name);
    self->name = name;
    Py_INCREF(value);
    self->value = value;
    self->raw_value = raw_value;

    return (PyObject *)self;
}

// create a new Type object without error checking
//
// py_type should be the Token type
//
// this function steals a reference to name
WooshType *
WooshType_NEW(PyTypeObject *py_type, PyObject *name, unsigned char raw_value)
{
    assert(PyType_Check(py_type));
    assert(PyUnicode_CheckExact(name));

    WooshType *self = (WooshType *)PyType_GenericAlloc(py_type, 0);
    if (!self)
    {
        // LCOV_EXCL_START
        Py_DECREF(name);
        return 0;
        // LCOV_EXCL_STOP
    }

    PyObject *value = PyLong_FromLong(raw_value);
    if (!value)
    {
        // LCOV_EXCL_START
        Py_DECREF(self);
        Py_DECREF(name);
        return 0;
        // LCOV_EXCL_STOP
    }

    self->name = name;
    self->value = value;
    self->raw_value = raw_value;

    return self;
}

// gets the name for the Type
PyObject *
WooshType_GetName(PyObject *self)
{
    if (WooshType_Check(self))
    {
        return (PyObject *)WooshType_GET_NAME((WooshType *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Type");
}

// gets the name for the Type without error checking
PyObject *
WooshType_GET_NAME(WooshType *self)
{
    assert(WooshType_Check((PyObject *)self));
    return self->name;
}

// get the value for the Type
PyObject *
WooshType_GetValue(PyObject *self)
{
    if (WooshType_Check(self))
    {
        return (PyObject *)WooshType_GET_VALUE((WooshType *)self);
    }
    return PyErr_Format(PyExc_TypeError, "expected a woosh.Type");
}

// get the value for the Type without error checking
PyObject *
WooshType_GET_VALUE(WooshType *self)
{
    assert(WooshType_Check((PyObject *)self));
    return self->value;
}

// get the c value for the Type
unsigned char
WooshType_GetRawValue(PyObject *self)
{
    if (WooshType_Check(self))
    {
        return WooshType_GET_RAW_VALUE((WooshType *)self);
    }
    PyErr_Format(PyExc_TypeError, "expected a woosh.Type");
    return 0;
}

// get the c value for the Type without error checking
unsigned char
WooshType_GET_RAW_VALUE(WooshType *self)
{
    assert(WooshType_Check((PyObject *)self));
    return self->raw_value;
}
