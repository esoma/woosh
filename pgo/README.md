This directory contains scripts for building `woosh` with profile guided
optimizations.

Simply run the correct `build-XXX.YY` file appropriate for your platform and
compiler. The PGO version of the C extension will be built in `../build`.

The scripts are fairly simple, executing a few major steps:
- set up a virtual environment and activate it
- build and install woosh with PGO instrumentation
- run generate-pgo-data.py for the PGO dataset
- build woosh using the PGO dataset for optimizations
