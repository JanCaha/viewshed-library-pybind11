#!/bin/bash

set -e  # Exit on any error

if ! git diff --cached --name-only | grep -q '^pyproject.toml'; then
    echo "⏭️ pyproject.toml not staged for commit. No need to update versions."
    exit 0
fi


PYTHON_PACKAGE_VERSION=$(grep '^version = ' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/')

print_info "Project version: $PYTHON_PACKAGE_VERSION"

sed -i '/^project(/s/[0-9]\+\.[0-9]\+\.[0-9]\+/'$PYTHON_PACKAGE_VERSION'/' CMakeLists.txt
sed -i '/version: /c\  version: \"'$PYTHON_PACKAGE_VERSION'\"' conda/meta.yaml

CONDA_VERSION=$(grep "version: " conda/meta.yaml | grep -E -o -e "[0-9\.]+")

if [[ "$CONDA_VERSION" != "$PYTHON_PACKAGE_VERSION" ]]; then
    echo "❌ Version mismatch between pyproject.toml and conda/meta.yaml"
    exit 1
fi

echo "Version updated! ✨"

