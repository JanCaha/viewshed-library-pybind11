#!/bin/bash
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DWITH_PY_STUBS=ON
cmake --build build --config Release