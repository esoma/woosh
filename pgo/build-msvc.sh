#!/usr/bin/env bash

DIR=$(pwd)

python -m venv "$DIR/_pgoenv"
if [[ $? != 0 ]]; then
    echo "Failed to setup virtual environment."
    exit 1
fi
source "$DIR/_pgoenv/scripts/activate"

(cd .. && python setup.py build_ext --pgo-generate -f --pgo-data "$DIR/woosh.pgd" install)
if [[ $? != 0 ]]; then
    echo "Failed to build instrumented."
    exit 1
fi

EXTENSION_LOCATION=$(python -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)")
if [[ $? != 0 ]]; then
    echo "Failed to find c-extension."
    exit 1
fi
cp "$DIR/woosh.pgd" "$EXTENSION_LOCATION/woosh.pgd"
if [[ $? != 0 ]]; then
    echo "Failed to copy pgd."
    exit 1
fi

python generate-pgo-data.py
if [[ $? != 0 ]]; then
    echo "Failed to generate PGO data."
    exit 1
fi

(cd .. && python setup.py build_ext --pgo-use --pgo-data "$EXTENSION_LOCATION/woosh.pgd" -f)
if [[ $? != 0 ]]; then
    echo "Failed to build PGO."
    exit 1
fi
