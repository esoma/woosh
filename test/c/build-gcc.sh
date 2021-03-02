#!/usr/bin/env bash

echo "Building woosh C tests..."

mkdir build

GCC_COV_FLAGS="-fprofile-arcs -ftest-coverage -fprofile-dir=build"

PYTHON_INCLUDES=$(python3-config --includes)
echo "PYTHON_INCLUDES=${PYTHON_INCLUDES}"

PYTHON_LIBS=$(python3-config --libs --embed)
if [[ $? != 0 ]]; then
    PYTHON_LIBS=$(python3-config --libs)
fi
echo "PYTHON_LIBS=${PYTHON_LIBS}"

PYTHON_LIBDIRS=""
for LDFLAG in $(python3-config --ldflags); do
    if [[ ${LDFLAG} == -L* ]]; then
        PYTHON_LIBDIRS="${PYTHON_LIBDIRS} ${LDFLAG}"
    fi
done
echo "PYTHON_LIBDIRS=${PYTHON_LIBDIRS}"

WOOSH_LIB_DIR=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)")
echo "WOOSH_LIB_DIR=${WOOSH_LIB_DIR}"

WOOSH_LIB=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).name)")
echo "WOOSH_LIB=${WOOSH_LIB}"

gcc ${GCC_COV_FLAGS} -o build/test_fifobuffer -I ../../src/ ../../src/fifobuffer.c internal/test_fifobuffer.c
gcc ${GCC_COV_FLAGS} -o build/test_lifobuffer -I ../../src/ ../../src/lifobuffer.c internal/test_lifobuffer.c
gcc ${GCC_COV_FLAGS} -o build/test_module_get -Wl,-rpath="${WOOSH_LIB_DIR}" -I ../../inc/ ${PYTHON_LIBDIRS} ${PYTHON_INCLUDES} -L ${WOOSH_LIB_DIR} api/base.c api/test_module_get.c -l:"${WOOSH_LIB}" ${PYTHON_LIBS} 
