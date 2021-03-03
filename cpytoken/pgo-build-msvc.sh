#!/usr/bin/env bash

DIR=$(pwd)

python -m venv "$DIR/_pgoenv"
source "$DIR/_pgoenv/scripts/activate"

python setup.py build_ext --pgo-generate -f --pgo-data "$DIR/_woosh_cpytoken.pgd" install

EXTENSION_LOCATION=$(python -c "import _woosh_cpytoken; import pathlib; print(pathlib.Path(_woosh_cpytoken.__file__).parent)")
cp "$DIR/_woosh_cpytoken.pgd" "$EXTENSION_LOCATION/_woosh_cpytoken.pgd"

python generate-pgo-data.py

python setup.py build_ext --pgo-use --pgo-data "$EXTENSION_LOCATION/_woosh_cpytoken.pgd" -f
