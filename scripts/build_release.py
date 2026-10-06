#!/usr/bin/env python3
"""Build a deterministic, allowlisted skill ZIP and SHA256SUMS (standard library only)."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

from validate_project import SKILL_NAME, markdown_targets, validate_project


PAYLOAD_FILES = (
    "SKILL.md", "VERSION", "LICENSE", "NOTICE.md", "scripts/access_probe.py",
    "tests/test_access_probe.py",
)
PAYLOAD_TREES = {"agents": {".yaml", ".yml"}, "references": {".md"}}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644


def payload_files(root):
    root = Path(root).resolve()
    selected = []
    for name in PAYLOAD_FILES:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("Missing or symlinked payload file: " + name)
        selected.append(path)
    for directory, suffixes in PAYLOAD_TREES.items():
        base = root / directory
        if base.is_symlink() or not base.is_dir():
            raise ValueError("Missing or symlinked payload directory: " + directory)
        for path in sorted(base.rglob("*")):
            if path.is_symlink():
                raise ValueError("Symlink in payload: " + path.relative_to(root).as_posix())
            if path.is_file():
                if any(part.startswith(".") for part in path.relative_to(base).parts):
                    raise ValueError("Hidden file in payload: " + path.relative_to(root).as_posix())
                if path.suffix not in suffixes:
                    raise ValueError("Unexpected payload file type: " + path.relative_to(root).as_posix())
                selected.append(path)
    return sorted(selected, key=lambda path: path.relative_to(root).as_posix())


def check_payload_links(root, payload):
    """Reject links that work in the repository but would break after ZIP installation."""
    names = set(payload)
    for name, data in payload.items():
        if not name.endswith(".md"):
            continue
        for target in markdown_targets(data.decode("utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            local = unquote(parsed.path)
            path = (root / local.lstrip("/") if local.startswith("/")
                    else (root / name).parent / local).resolve()
            try:
                relative = path.relative_to(root).as_posix()
            except ValueError as error:
                raise ValueError("Payload link leaves skill: " + name + " -> " + target) from error
            if relative not in names and not any(item.startswith(relative.rstrip("/") + "/") for item in names):
                raise ValueError("Payload link targets an excluded file: " + name + " -> " + target)


def verify_archive(archive_path, payload):
    expected = {SKILL_NAME + "/" + name: data for name, data in payload.items()}
    with zipfile.ZipFile(archive_path) as archive:
        if archive.namelist() != sorted(expected):
            raise ValueError("Archive entry list differs from the explicit payload")
        if archive.testzip() is not None:
            raise ValueError("Archive CRC check failed")
        for info in archive.infolist():
            if (info.date_time != FIXED_TIME or info.create_system != 3
                    or info.external_attr >> 16 != FILE_MODE
                    or info.compress_type != zipfile.ZIP_STORED or info.extra):
                raise ValueError("Unexpected archive metadata: " + info.filename)
            actual = hashlib.sha256(archive.read(info.filename)).digest()
            if actual != hashlib.sha256(expected[info.filename]).digest():
                raise ValueError("Archive content hash mismatch: " + info.filename)


def build_release(root, output_dir=None):
    root = Path(root).resolve()
    errors = validate_project(root)
    if errors:
        raise ValueError("Project validation failed:\n" + "\n".join(errors))
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    payload = {path.relative_to(root).as_posix(): path.read_bytes() for path in payload_files(root)}
    check_payload_links(root, payload)
    output_dir = Path(output_dir).resolve() if output_dir is not None else root / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = SKILL_NAME + "-v" + version + ".zip"
    destination = output_dir / filename
    # ZIP_STORED also avoids cross-version zlib output differences. The payload is small.
    with tempfile.TemporaryDirectory(prefix=".aaa-release-", dir=output_dir) as temporary:
        candidate = Path(temporary) / filename
        with zipfile.ZipFile(candidate, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, data in payload.items():
                info = zipfile.ZipInfo(SKILL_NAME + "/" + name, FIXED_TIME)
                info.create_system = 3
                info.external_attr = FILE_MODE << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, data)
        verify_archive(candidate, payload)
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        sums = Path(temporary) / "SHA256SUMS"
        sums.write_bytes((digest + "  " + filename + "\n").encode("ascii"))
        os.replace(candidate, destination)
        os.replace(sums, output_dir / "SHA256SUMS")
    return {"version": version, "archive": str(destination),
            "checksum_file": str(output_dir / "SHA256SUMS"),
            "sha256": digest, "payload_files": len(payload)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)
    try:
        result = build_release(args.root, args.output_dir)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
