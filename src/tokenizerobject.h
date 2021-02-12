#ifndef WOOSH_TOKENIZEROBJECTH
#define WOOSH_TOKENIZEROBJECTH

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "tokenobject.h"

struct WooshTokenizer_;
typedef struct WooshTokenizer_ WooshTokenizer;

PyTypeObject *WooshTokenizer_Initialize_(PyObject *);

WooshTokenizer *WooshTokenizer_New_(PyObject *, PyObject *);
PyTypeObject *WooshTokenizer_Get_();

int WooshTokenizer_Check(PyObject *);
int WooshTokenizer_CheckExact(PyObject *);

PyObject *WooshTokenizer_Next(PyObject *);
WooshToken *WooshTokenizer_NEXT(WooshTokenizer *);

#endif
