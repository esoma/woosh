#!/usr/bin/env bash

case $(uname) in
    *"_NT"*)
        source ./pgo-build-msvc.sh
        ;;
    *)
        source ./pgo-build-cc.sh
        ;;
esac
