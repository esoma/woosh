
// woosh
#include "module.h"
#include "modulestate.h"
#include "tokenobject.h"
#include "tokenizerobject.h"
#include "typeobject.h"

static PyObject *
woosh_module_tokenize(PyObject *self, PyObject *args)
{
    PyObject *source;
    if (!PyArg_ParseTuple(args, "O", &source)){ return 0; };
    return (PyObject *)WooshTokenizer_New_(self, source);
}

static int
woosh_module_traverse(PyObject *self, visitproc visit, void *arg)
{
    struct WooshModuleState *state = PyModule_GetState(self);
    assert(state);
    return WooshModuleState_Traverse_(state, visit, arg);
}

static int
woosh_module_clear(PyObject *self)
{
    struct WooshModuleState *state = PyModule_GetState(self);
    assert(state);
    return WooshModuleState_Clear_(state);
}

static PyMethodDef woosh_module_methods[] = {
    {"tokenize",  woosh_module_tokenize, METH_VARARGS, 0},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef woosh_module = {
    PyModuleDef_HEAD_INIT,
    "_woosh",
    0,
    sizeof(struct WooshModuleState),
    woosh_module_methods,
    0,
    woosh_module_traverse,
    woosh_module_clear
};

PyMODINIT_FUNC
PyInit__woosh()
{
    PyObject *module = PyModule_Create(&woosh_module);
    if (!module){ goto error; }

    if (PyState_AddModule(module, &woosh_module) == -1){ goto error; }

    struct WooshModuleState *state = PyModule_GetState(module);
    assert(state);

    state->token = WooshToken_Initialize_(module);
    if (!state->token){ goto error; }
    Py_INCREF(state->token);

    state->tokenizer = WooshTokenizer_Initialize_(module);
    if (!state->tokenizer){ goto error; }

    state->type = WooshType_Initialize_(module);
    if (!state->type){ goto error; }
    Py_INCREF(state->type);

    {
        unsigned char i = 0;

#define WOOSHTYPE_ADD(destination, name)\
        assert(destination == 0);\
        destination = WooshType_Add_(module, name, i);\
        if (!destination){ goto error; }\
        i += 1;\
        Py_INCREF(destination);

        WOOSHTYPE_ADD(state->newline_type, "NEWLINE");
        WOOSHTYPE_ADD(state->nl_type, "NL");
        WOOSHTYPE_ADD(state->operator_type, "OP");
        WOOSHTYPE_ADD(state->indent_type, "INDENT");
        WOOSHTYPE_ADD(state->dedent_type, "DEDENT");
        WOOSHTYPE_ADD(state->name_type, "NAME");
        WOOSHTYPE_ADD(state->number_type, "NUMBER");
        WOOSHTYPE_ADD(state->string_type, "STRING");
        WOOSHTYPE_ADD(state->comment_type, "COMMENT");
        WOOSHTYPE_ADD(state->eof_type, "EOF");
        WOOSHTYPE_ADD(state->error_type, "ERROR");
        WOOSHTYPE_ADD(state->encoding_type, "ENCODING");
#undef WOOSHTYPE_ADD
    }

    return module;
error:
    Py_CLEAR(module);
    return 0;
}

PyObject *
WooshModule_Get()
{
    PyObject *module = PyState_FindModule(&woosh_module);
    if (!module)
    {
        return PyErr_Format(PyExc_RuntimeError, "woosh module not ready");
    }
    return module;
}
