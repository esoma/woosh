#!/usr/bin/env bash

GCC_COV_FLAGS="-fprofile-arcs -ftest-coverage"
PYTHON_INCLUDES=$(python3-config --includes)
PYTHON_LIBS=$(python3-config --libs)
WOOSH_LIB_DIR=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)")
WOOSH_LIB=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).name)")

gcc ${GCC_COV_FLAGS} -o test_fifobuffer -I ../../src/ ../../src/fifobuffer.c test_fifobuffer.c
gcc ${GCC_COV_FLAGS} -o test_lifobuffer -I ../../src/ ../../src/lifobuffer.c test_lifobuffer.c
gcc ${GCC_COV_FLAGS} -o test_module_get -Wl,-rpath="${WOOSH_LIB_DIR}" -I ../../inc/ ${PYTHON_INCLUDES} -L ${WOOSH_LIB_DIR} capi_test_base.c test_module_get.c -l:"${WOOSH_LIB}" ${PYTHON_LIBS} 
