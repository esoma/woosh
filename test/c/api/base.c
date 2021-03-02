
// c
#include <stdio.h>
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>

int test_main();

int
main(int argc, char *argv[])
{
    Py_Initialize();
    int result = test_main();
    if (Py_FinalizeEx() < 0){ return EXIT_FAILURE; }
    return result;
}
