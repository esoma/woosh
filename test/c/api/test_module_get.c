
// c
#include <stdio.h>
// woosh
#include <woosh.h>

int
test_main()
{
    {
        fprintf(stderr, "WooshModule_Get raises RuntimError if module is not imported...");
        PyObject *module = WooshModule_Get();
        assert(module == 0);
        assert(PyErr_Occurred());
        assert(PyErr_ExceptionMatches(PyExc_RuntimeError));
        PyErr_Clear();
        fprintf(stderr, "passed\n");
    }
    
    {
        fprintf(stderr, "WooshModule_Get returns the _woosh module once imported...");
        PyObject *py_module = PyImport_ImportModule("woosh");
        if (!py_module)
        {
            fprintf(stderr, "failed to import woosh, is it installed?\n");
            return EXIT_FAILURE;
        }
        {
            PyObject *py_name = PyObject_GetAttrString(py_module, "__name__");
            assert(py_name != 0);
            assert(PyUnicode_CompareWithASCIIString(py_name, "woosh") == 0);
            Py_DECREF(py_name);
        }
        fprintf(stderr, "passed\n");
        
        {
            PyObject *c_module = WooshModule_Get();
            assert(c_module != 0);
            assert(!PyErr_Occurred());
            assert(py_module != c_module);
            {
                PyObject *c_name = PyObject_GetAttrString(c_module, "__name__");
                assert(c_name != 0);
                assert(PyUnicode_CompareWithASCIIString(c_name, "_woosh") == 0);
                Py_DECREF(c_name);
            }
            
            fprintf(stderr, "WooshModule_Get returns borrowed ref...");
            size_t c_module_ref_count = Py_REFCNT(c_module);
            WooshModule_Get();
            assert(Py_REFCNT(c_module) == c_module_ref_count);
        }
        
        Py_DECREF(py_module);
        
        fprintf(stderr, "passed\n");
    }
    
    return EXIT_SUCCESS;
}
