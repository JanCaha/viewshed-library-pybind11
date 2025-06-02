#!/bin/bash

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_error() {
    echo -e "{RED}[ERROR]${NC} $1"
}

echo "🔍 Running pre-commit checks..."

PYTHON_PACKAGE_VERSION=$(grep '^version = ' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/')

print_info "Project version: $PYTHON_PACKAGE_VERSION"

sed -i '/^project(/s/[0-9]\+\.[0-9]\+\.[0-9]\+/'$PYTHON_PACKAGE_VERSION'/' CMakeLists.txt
sed -i '/version: /c\  version: \"'$PYTHON_PACKAGE_VERSION'\"' conda/meta.yaml

CONDA_VERSION=$(grep "version: " conda/meta.yaml | grep -E -o -e "[0-9\.]+")

if [[ "$CONDA_VERSION" != "$PYTHON_PACKAGE_VERSION" ]]; then
    print_error "${RED}[ERROR]${NC} Version mismatch between pyproject.toml and conda/meta.yaml"
    exit 1
fi

print_success "Version updated! ✨"

