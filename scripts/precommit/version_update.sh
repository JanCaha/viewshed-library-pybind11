#!/bin/bash

set -e  # Exit on any error

FILES=$(git diff --cached --name-only | grep -E '^pyproject.toml$')

if [ -z "$FILES" ]; then
    exit 0
fi

PYTHON_PACKAGE_VERSION=$(grep '^version = ' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/')

echo -e "Project version: $PYTHON_PACKAGE_VERSION"

sed -i '/^project(/s/[0-9]\+\.[0-9]\+\.[0-9]\+/'$PYTHON_PACKAGE_VERSION'/' CMakeLists.txt
sed -i '/version: /c\  version: \"'$PYTHON_PACKAGE_VERSION'\"' conda/meta.yaml
