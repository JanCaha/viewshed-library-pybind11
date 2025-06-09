#!/bin/bash

if ! git diff --cached --name-only | grep -q '^src/'; then
    exit 0
fi

cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DWITH_PY_STUBS=ON
cmake --build build --config Release