#ifndef WOOSH_MODULESTATEH
#define WOOSH_MODULESTATEH

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// woosh
#include "_woosh/typeobject.h"

// per-interpreter module state
struct WooshModuleState
{
    // extension types defined on the module
    PyTypeObject *type;
    PyTypeObject *token;
    PyTypeObject *tokenizer;
    // all the type instances defined on the module
    WooshType *newline_type;
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
};

struct WooshModuleState *WooshModuleState_Get_();
int WooshModuleState_Traverse_(struct WooshModuleState *, visitproc, void *);
int WooshModuleState_Clear_(struct WooshModuleState *);

#endif
