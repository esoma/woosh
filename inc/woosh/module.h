#ifndef WOOSH_MODULEH
#define WOOSH_MODULEH

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "woosh/expose.h"

WOOSH_EXPOSE
PyObject *WooshModule_Get();

#endif
