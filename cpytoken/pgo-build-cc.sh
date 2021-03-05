#!/usr/bin/env bash

DIR=$(pwd)

python3 -m venv "$DIR/_pgoenv"
if [[ $? != 0 ]]; then
    echo "Failed to setup virtual environment."
    exit $?
fi
source "$DIR/_pgoenv/bin/activate"

python3 setup.py build_ext --pgo-generate -f --pgo-data "$DIR" install

python3 generate-pgo-data.py

python3 setup.py build_ext --pgo-use --pgo-data "$DIR" -f
