#!/usr/bin/env python3
"""Snapshot the current KeepRight spec and schemas into versioned copies."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec.json"
VERSIONS_DIR = ROOT / "versions"
SCHEMAS_DIR = ROOT / "schemas"

SCHEMA_FILES = [
    "keepright-spec",
    "keepright-declaration",
]


def read_spec_meta() -> dict[str, str]:
    with SPEC_PATH.open("r", encoding="utf-8") as source:
        spec = json.load(source)

    meta = spec.get("meta")
    if not isinstance(meta, dict):
        raise ValueError("spec.json must have a meta object")

    spec_version = meta.get("specVersion")
    schema_version = meta.get("schemaVersion")
    if not isinstance(spec_version, str) or not spec_version:
        raise ValueError("spec.json meta.specVersion must be a string")
    if not isinstance(schema_version, str) or not schema_version:
        raise ValueError("spec.json meta.schemaVersion must be a string")

    return {
        "specVersion": spec_version,
        "schemaVersion": schema_version,
    }


def version_parts(version: str) -> tuple[str, str, str]:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"Expected MAJOR.MINOR.PATCH version, got {version!r}")

    return parts[0], parts[1], parts[2]


def files_match(source: Path, target: Path) -> bool:
    return source.read_bytes() == target.read_bytes()


def copy_exact(source: Path, target: Path) -> str:
    if target.exists():
        if files_match(source, target):
            return f"ok existing {target.relative_to(ROOT)}"

        raise ValueError(
            f"{target.relative_to(ROOT)} already exists but does not match {source.relative_to(ROOT)}. "
            "Bump the relevant version before creating a new snapshot."
        )

    shutil.copy2(source, target)
    return f"created {target.relative_to(ROOT)}"


def copy_latest(source: Path, target: Path) -> str:
    changed = not target.exists() or not files_match(source, target)
    shutil.copy2(source, target)
    action = "updated" if changed else "ok current"
    return f"{action} {target.relative_to(ROOT)}"


def snapshot_spec(spec_version: str) -> list[str]:
    major, minor, _patch = version_parts(spec_version)
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

    messages = [
        copy_exact(SPEC_PATH, VERSIONS_DIR / f"spec.{spec_version}.json"),
        copy_latest(SPEC_PATH, VERSIONS_DIR / f"spec.{major}.{minor}.latest.json"),
        copy_latest(SPEC_PATH, VERSIONS_DIR / f"spec.{major}.latest.json"),
        copy_latest(SPEC_PATH, VERSIONS_DIR / "spec.latest.json"),
    ]

    return messages


def snapshot_schema(schema_name: str, schema_version: str) -> list[str]:
    major, minor, _patch = version_parts(schema_version)
    source = SCHEMAS_DIR / f"{schema_name}.schema.json"
    if not source.exists():
        raise FileNotFoundError(f"Missing schema source {source.relative_to(ROOT)}")

    return [
        copy_exact(source, SCHEMAS_DIR / f"{schema_name}.{schema_version}.schema.json"),
        copy_latest(source, SCHEMAS_DIR / f"{schema_name}.{major}.{minor}.latest.schema.json"),
        copy_latest(source, SCHEMAS_DIR / f"{schema_name}.{major}.latest.schema.json"),
        copy_latest(source, SCHEMAS_DIR / f"{schema_name}.latest.schema.json"),
    ]


def main() -> None:
    versions = read_spec_meta()

    print(f"Spec version: {versions['specVersion']}")
    print(f"Schema version: {versions['schemaVersion']}")

    for message in snapshot_spec(versions["specVersion"]):
        print(message)

    for schema_name in SCHEMA_FILES:
        for message in snapshot_schema(schema_name, versions["schemaVersion"]):
            print(message)


if __name__ == "__main__":
    main()
