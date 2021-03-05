#!/usr/bin/env bash

_CC_COV_FLAGS="-fprofile-arcs -ftest-coverage"

echo "Discovering environment..."

if [[ -z "$CC" ]]; then
    CC=gcc
fi

mkdir -p build
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to create build directory."
    exit $RETVAL
fi

PYTHON_INCLUDES=$(python3-config --includes)
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to get python include compilation flags."
    exit $RETVAL
fi
echo "    PYTHON_INCLUDES=${PYTHON_INCLUDES}"

PYTHON_LIBS=$(python3-config --libs --embed)
if [[ $? != 0 ]]; then
    PYTHON_LIBS=$(python3-config --libs)
    if [[ $? != 0 ]]; then
        RETVAL=$?
        echo "Failed to get python lib compilation flags."
        exit $RETVAL
    fi
fi
echo "    PYTHON_LIBS=${PYTHON_LIBS}"

PYTHON_LIBDIRS=""
_=$(python3-config --ldflags);
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to get python lib compilation flags."
    exit $RETVAL
fi
for LDFLAG in $_; do
    if [[ ${LDFLAG} == -L* ]]; then
        PYTHON_LIBDIRS="${PYTHON_LIBDIRS} ${LDFLAG}"
    fi
done
echo "    PYTHON_LIBDIRS=${PYTHON_LIBDIRS}"

WOOSH_LIB_DIR=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)")
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to get woosh lib directory."
    exit $RETVAL
fi
echo "    WOOSH_LIB_DIR=${WOOSH_LIB_DIR}"

WOOSH_LIB=$(python3 -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).name)")
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to get woosh lib name."
    exit $RETVAL
fi
echo "    WOOSH_LIB=${WOOSH_LIB}"


echo "Discovering tests to build..."

API_TESTS=$(find ./api -name "test_*.c")
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to find API tests."
    exit $RETVAL
fi
for TEST in $API_TESTS; do
    echo "    $TEST"
done

INTERNAL_TESTS=$(find ./internal -name "test_*.c")
if [[ $? != 0 ]]; then
    RETVAL=$?
    echo "Failed to find internal tests."
    exit $RETVAL
fi
for TEST in $INTERNAL_TESTS; do
    echo "    $TEST"
done


echo "Building API tests..."
for TEST in $API_TESTS; do

    TEST_NAME=$(basename $TEST .c)
    if [[ $? != 0 ]]; then
        RETVAL=$?
        echo "Failed to get test name."
        exit $RETVAL
    fi
    
    echo "    Building $TEST_NAME..."
    
    "$CC" ${_CC_COV_FLAGS} -o "build/${TEST_NAME}"\
        -Wl,-rpath="${WOOSH_LIB_DIR}" -I ../../inc/\
        ${PYTHON_LIBDIRS} ${PYTHON_INCLUDES} -L ${WOOSH_LIB_DIR}\
        api/base.c "${TEST}" -l:"${WOOSH_LIB}" ${PYTHON_LIBS}
    if [[ $? != 0 ]]; then
        RETVAL=$?
        echo "Failed to build test."
        exit $RETVAL
    fi
    
done


echo "Building internal tests..."
for TEST in $INTERNAL_TESTS; do

    TEST_NAME=$(basename $TEST .c)
    if [[ $? != 0 ]]; then
        RETVAL=$?
        echo "Failed to get test name."
        exit $RETVAL
    fi
    
    echo "    Building $TEST_NAME..."
    
    "$CC" ${_CC_COV_FLAGS} -o "build/${TEST_NAME}" -I ../../src/_woosh/ "${TEST}"
    if [[ $? != 0 ]]; then
        RETVAL=$?
        echo "Failed to build test."
        exit $RETVAL
    fi
    
done

echo "Done...use ./test.sh to run tests."
