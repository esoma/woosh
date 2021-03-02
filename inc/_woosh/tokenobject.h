#ifndef WOOSH_TOKENOBJECT_H
#define WOOSH_TOKENOBJECT_H

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "_woosh/typeobject.h"

struct WooshToken_;
typedef struct WooshToken_ WooshToken;

PyTypeObject *WooshToken_Initialize_(PyObject *);

PyTypeObject *WooshToken_Get();

int WooshToken_Check(PyObject *);
int WooshToken_CheckExact(PyObject *);

PyObject *WooshToken_New(
    PyObject *, PyObject *,
    PyObject *, PyObject *,
    PyObject *, PyObject *
);
WooshToken *WooshToken_NEW(
    PyTypeObject *,
    WooshType*, PyObject*,
    PyObject*, PyObject*,
    PyObject*, PyObject*
);

PyObject *WooshToken_GetType(PyObject *);
WooshType *WooshToken_GET_TYPE(WooshToken *);

PyObject *WooshToken_GetValue(PyObject *);
PyObject *WooshToken_GET_VALUE(WooshToken *);

PyObject *WooshToken_GetStartLine(PyObject *);
PyObject *WooshToken_GET_START_LINE(WooshToken *);

PyObject *WooshToken_GetStartColumn(PyObject *);
PyObject *WooshToken_GET_START_COLUMN(WooshToken *);

PyObject *WooshToken_GetEndLine(PyObject *);
PyObject *WooshToken_GET_END_LINE(WooshToken *);

PyObject *WooshToken_GetEndColumn(PyObject *);
PyObject *WooshToken_GET_END_COLUMN(WooshToken *);

#endif
