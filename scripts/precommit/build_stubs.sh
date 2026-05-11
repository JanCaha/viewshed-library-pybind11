#!/bin/bash

if ! git diff --cached --name-only | grep -q '^cpp_module/'; then
    exit 0
fi

cmake --workflow --preset workflow-release-stubs