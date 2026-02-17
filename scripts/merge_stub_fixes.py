#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


CLASS_RE = re.compile(r"^class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*$")
DEF_RE = re.compile(r"^(?P<indent>\s*)def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(")


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _index_defs(lines: list[str]) -> dict[tuple[str, str, int], str]:
    indexed: dict[tuple[str, str, int], str] = {}
    counters: dict[tuple[str, str], int] = {}
    current_class = ""

    for line in lines:
        class_match = CLASS_RE.match(line)
        if class_match:
            current_class = class_match.group("name")
            continue

        def_match = DEF_RE.match(line)
        if not def_match:
            continue

        method_name = def_match.group("name")
        base_key = (current_class, method_name)
        index = counters.get(base_key, 0)
        counters[base_key] = index + 1
        indexed[(current_class, method_name, index)] = line

    return indexed


def _extract_top_alias_block(lines: list[str]) -> list[str]:
    all_idx = next((i for i, line in enumerate(lines) if line.startswith("__all__ = ")), None)
    first_class_idx = next((i for i, line in enumerate(lines) if line.startswith("class ")), None)

    if all_idx is None or first_class_idx is None or first_class_idx <= all_idx + 1:
        return []

    start = all_idx + 1
    while start < first_class_idx and lines[start].strip() == "":
        start += 1

    if start >= first_class_idx:
        return []

    end = first_class_idx
    while end > start and lines[end - 1].strip() == "":
        end -= 1

    if end <= start:
        return []

    block = lines[start:end]
    return block + ["\n"]


def merge_stub(generated: Path, existing: Path, output: Path) -> None:
    generated_lines = _read_lines(generated)

    if not existing.exists():
        output.write_text("".join(generated_lines), encoding="utf-8")
        return

    existing_lines = _read_lines(existing)
    existing_defs = _index_defs(existing_lines)

    merged_lines: list[str] = []
    current_class = ""
    counters: dict[tuple[str, str], int] = {}

    for line in generated_lines:
        class_match = CLASS_RE.match(line)
        if class_match:
            current_class = class_match.group("name")
            merged_lines.append(line)
            continue

        def_match = DEF_RE.match(line)
        if not def_match:
            merged_lines.append(line)
            continue

        method_name = def_match.group("name")
        base_key = (current_class, method_name)
        index = counters.get(base_key, 0)
        counters[base_key] = index + 1

        merged_lines.append(existing_defs.get((current_class, method_name, index), line))

    alias_block = _extract_top_alias_block(existing_lines)
    if alias_block:
        all_idx = next((i for i, line in enumerate(merged_lines) if line.startswith("__all__ = ")), None)
        first_class_idx = next((i for i, line in enumerate(merged_lines) if line.startswith("class ")), None)
        if all_idx is not None and first_class_idx is not None and first_class_idx > all_idx:
            start = all_idx + 1
            while start < first_class_idx and merged_lines[start].strip() == "":
                start += 1
            merged_lines = merged_lines[:start] + alias_block + merged_lines[first_class_idx:]

    merged_text = "".join(merged_lines)
    merged_text = merged_text.replace("Specifiy", "Specify")
    output.write_text(merged_text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge generated pybind11 stubs with existing manual stub edits.")
    parser.add_argument("--generated", type=Path, required=True, help="Path to generated .pyi file")
    parser.add_argument("--existing", type=Path, required=True, help="Path to existing curated .pyi file")
    parser.add_argument("--output", type=Path, required=True, help="Output path for merged .pyi file")
    args = parser.parse_args()

    merge_stub(args.generated, args.existing, args.output)


if __name__ == "__main__":
    main()
