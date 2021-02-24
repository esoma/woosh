#!/usr/bin/env bash

DIR=$(pwd)

python -m venv "$DIR/_pgoenv"
source "$DIR/_pgoenv/scripts/activate"

cd ..
python setup.py build_ext --pgo-generate -f --pgo-data "$DIR/woosh.pgd" install
cd "$DIR"

EXTENSION_LOCATION=$(python -c "import _woosh; import pathlib; print(pathlib.Path(_woosh.__file__).parent)")
cp "$DIR/woosh.pgd" "$EXTENSION_LOCATION/woosh.pgd"

python generate-pgo-data.py

cd ..
python setup.py build_ext --pgo-use --pgo-data "$EXTENSION_LOCATION/woosh.pgd" -f
cd "$DIR"
