
// woosh
#include "module.h"
#include "modulestate.h"

// get the ModuleState for woosh
struct WooshModuleState *
WooshModuleState_Get_()
{
    PyObject *module = WooshModule_Get();
    if (!module){ return 0; }
    return (struct WooshModuleState *)PyModule_GetState(module);
}

int
WooshModuleState_Traverse_(
    struct WooshModuleState *self,
    visitproc visit,
    void *arg
)
{
    Py_VISIT(self->type);
    Py_VISIT(self->token);
    Py_VISIT(self->tokenizer);

    Py_VISIT(self->newline_type);
    Py_VISIT(self->nl_type);
    Py_VISIT(self->operator_type);
    Py_VISIT(self->indent_type);
    Py_VISIT(self->dedent_type);
    Py_VISIT(self->name_type);
    Py_VISIT(self->number_type);
    Py_VISIT(self->string_type);
    Py_VISIT(self->comment_type);
    Py_VISIT(self->eof_type);
    Py_VISIT(self->error_type);
    Py_VISIT(self->encoding_type);
    return 0;
}

int
WooshModuleState_Clear_(struct WooshModuleState *self)
{
    Py_CLEAR(self->type);
    Py_CLEAR(self->token);
    Py_CLEAR(self->tokenizer);

    Py_CLEAR(self->newline_type);
    Py_CLEAR(self->nl_type);
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
    return 0;
}
