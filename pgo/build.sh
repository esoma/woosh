#!/usr/bin/env bash

case $(uname) in
    *"_NT"*)
        source ./build-msvc.sh
        ;;
    *)
        source ./build-cc.sh
        ;;
esac
