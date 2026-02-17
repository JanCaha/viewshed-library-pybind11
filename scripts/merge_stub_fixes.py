#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


CLASS_RE = re.compile(r"^class\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\b.*:\s*$")
DEF_RE = re.compile(r"^(?P<indent>\s*)def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\b")


def _read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def _extract_def_block(lines: list[str], start: int) -> tuple[str, list[str], int]:
    def_match = DEF_RE.match(lines[start])
    if not def_match:
        raise ValueError("Expected function definition at start index")

    method_name = def_match.group("name")
    base_indent = len(def_match.group("indent"))
    end = start + 1

    while end < len(lines):
        line = lines[end]
        stripped = line.strip()

        if stripped == "":
            end += 1
            continue

        if CLASS_RE.match(line):
            break

        next_def_match = DEF_RE.match(line)
        if next_def_match and len(next_def_match.group("indent")) <= base_indent:
            break

        if line.lstrip().startswith("@") and (len(line) - len(line.lstrip())) <= base_indent:
            break

        end += 1

    return method_name, lines[start:end], end


def _index_defs(lines: list[str]) -> dict[tuple[str, str, int], list[str]]:
    indexed: dict[tuple[str, str, int], list[str]] = {}
    counters: dict[tuple[str, str], int] = {}
    current_class = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        class_match = CLASS_RE.match(line)
        if class_match:
            current_class = class_match.group("name")
            i += 1
            continue

        if not DEF_RE.match(line):
            i += 1
            continue

        method_name, def_block, next_index = _extract_def_block(lines, i)
        base_key = (current_class, method_name)
        index = counters.get(base_key, 0)
        counters[base_key] = index + 1
        indexed[(current_class, method_name, index)] = def_block
        i = next_index

    return indexed


def _extract_prefix_to_first_class(lines: list[str]) -> list[str]:
    first_class_idx = next((i for i, line in enumerate(lines) if line.startswith("class ")), None)
    if first_class_idx is None:
        return lines
    return lines[:first_class_idx]


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

    i = 0
    while i < len(generated_lines):
        line = generated_lines[i]
        class_match = CLASS_RE.match(line)
        if class_match:
            current_class = class_match.group("name")
            merged_lines.append(line)
            i += 1
            continue

        if not DEF_RE.match(line):
            merged_lines.append(line)
            i += 1
            continue

        method_name, generated_def_block, next_index = _extract_def_block(generated_lines, i)
        base_key = (current_class, method_name)
        index = counters.get(base_key, 0)
        counters[base_key] = index + 1

        merged_lines.extend(existing_defs.get((current_class, method_name, index), generated_def_block))
        i = next_index

    existing_prefix = _extract_prefix_to_first_class(existing_lines)
    if existing_prefix:
        first_class_idx = next((i for i, line in enumerate(merged_lines) if line.startswith("class ")), None)
        if first_class_idx is None:
            merged_lines = existing_prefix
        else:
            merged_lines = existing_prefix + merged_lines[first_class_idx:]

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
