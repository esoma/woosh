#!/usr/bin/env bash

DIR=$(pwd)

python3 -m venv "$DIR/_pgoenv"
if [[ $? != 0 ]]; then
    echo "Failed to setup virtual environment."
    exit 1
fi
source "$DIR/_pgoenv/bin/activate"

(cd .. && python3 setup.py build_ext --pgo-generate -f --pgo-data "$DIR" install)
if [[ $? != 0 ]]; then
    echo "Failed to build instrumented."
    exit 1
fi

python generate-pgo-data.py
if [[ $? != 0 ]]; then
    echo "Failed to generate PGO data."
    exit 1
fi

(cd .. && python3 setup.py build_ext --pgo-use --pgo-data "$DIR" -f)
if [[ $? != 0 ]]; then
    echo "Failed to build PGO."
    exit 1
fi
