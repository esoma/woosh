#ifndef WOOSH_TYPEOBJECT_H
#define WOOSH_TYPEOBJECT_H

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>

struct WooshType_;
typedef struct WooshType_ WooshType;

PyTypeObject *WooshType_Initialize_(PyObject *);
WooshType *WooshType_Add_(PyObject *, const char*, unsigned char);

PyTypeObject *WooshType_Get();

int WooshType_Check(PyObject *);
int WooshType_CheckExact(PyObject *);

PyObject *WooshType_New(PyObject *, PyObject *);
WooshType *WooshType_NEW(PyTypeObject *, PyObject*, unsigned char);

PyObject *WooshType_GetName(PyObject *);
PyObject *WooshType_GET_NAME(WooshType *);

PyObject *WooshType_GetValue(PyObject *);
PyObject *WooshType_GET_VALUE(WooshType *);

unsigned char WooshType_GetRawValue(PyObject *);
unsigned char WooshType_GET_RAW_VALUE(WooshType *);

#endif
