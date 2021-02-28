#!/usr/bin/env bash

gcc -fprofile-arcs -ftest-coverage -o test_fifobuffer -I ../../src/ ../../src/fifobuffer.c test_fifobuffer.c
gcc -fprofile-arcs -ftest-coverage -o test_lifobuffer -I ../../src/ ../../src/lifobuffer.c test_lifobuffer.c
