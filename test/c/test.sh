#!/usr/bin/env bash

RETVAL=0

for TEST in $(find . -name "test_*" ! -name "*.*"); do
    $(./$TEST)
    if [[ $? -ne 0 ]]; then
        RETVAL=1
    fi
done

exit $RETVAL