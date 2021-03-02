#ifndef WOOSH_MODULEH
#define WOOSH_MODULEH

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "_woosh/expose.h"

WOOSH_EXPOSE_
PyObject *WooshModule_Get();

#endif
