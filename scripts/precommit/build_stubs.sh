#!/bin/bash

if ! git diff --cached --name-only | grep -q '^src/'; then
    echo "⏭️ No files from the src directory are staged for commit. No need to rebuild stubs."
    exit 0
fi

cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DWITH_PY_STUBS=ON
cmake --build build --config Release