#!/usr/bin/env python3
"""Validate the repository and release inputs using only the Python standard library."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_NAME = "aaa-research"
REQUIRED_FILES = (
    "SKILL.md", "VERSION", "LICENSE", "NOTICE.md", "README.md", "README.zh-CN.md",
    "CONTRIBUTING.md", "CHANGELOG.md", "docs/VALIDATION.md", "agents/openai.yaml",
    "scripts/access_probe.py", "tests/test_access_probe.py",
)
IGNORED_PARTS = {".git", "dist", "__pycache__", ".venv", "venv", "work", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt", ".toml"}
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
                    r"(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?"
                    r"(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?\Z")
PRIVATE_PATH = re.compile(r"(?:/(?:Users|home)/|[A-Za-z]:[\\/]Users[\\/])"
                          r"([^/\\\s<>\"'`]+)")
GENERIC_USERS = {"user", "username", "your-user", "your-username", "example-user"}
UNFINISHED = re.compile(r"(?im)^\s*(?:[-*]\s+)?(?:TODO|FIXME|TBD)(?:\s*:|\s*$)"
                        r"|\[TODO(?:[ :][^\]]*)?\]|\{\{(?:TODO|PLACEHOLDER|REPLACE_ME)[^}]*\}\}")


def without_fences(text):
    """Keep prose checks separate from documented command/example placeholders."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            lines.append("")
        elif fence is None:
            lines.append(line)
        else:
            lines.append("")
    return "\n".join(lines)


def scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def skill_metadata(text):
    """Read this project's deliberately simple frontmatter, not arbitrary YAML."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error
    fields, current = {}, None
    version = None
    for line in lines[1:end]:
        top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top:
            current, value = top.groups()
            if current in fields:
                raise ValueError("Duplicate frontmatter field: " + current)
            fields[current] = scalar(value)
        elif current == "metadata":
            nested = re.match(r"^  version:\s*(.*)$", line)
            if nested:
                if version is not None:
                    raise ValueError("Duplicate metadata.version")
                version = scalar(nested.group(1))
    return fields, version


def project_files(root):
    """Inspect source files without traversing ignored artifacts or symlinks."""
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError("Symlinks are not release inputs: " + relative.as_posix())
        if path.is_file() and path.name != ".DS_Store":
            files.append(path)
    return files


def markdown_targets(text):
    """Extract inline and reference-style link destinations used by these docs."""
    text = without_fences(text)
    raw = re.findall(r"\]\((<[^>\n]+>|[^\s)]+)(?:\s+[^)]+)?\)", text)
    raw += re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(<[^>\n]+>|\S+)", text)
    return [target.strip("<>") for target in raw]


def validate_project(root):
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append("Missing required file: " + name)
    if not (root / "references").is_dir() or not list((root / "references").glob("*.md")):
        errors.append("references/ must contain Markdown research guidance")
    version = None
    if (root / "VERSION").is_file():
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if not SEMVER.fullmatch(version):
            errors.append("VERSION must contain one semantic version, such as 1.0.0")
    if (root / "SKILL.md").is_file():
        try:
            fields, declared_version = skill_metadata((root / "SKILL.md").read_text(encoding="utf-8"))
            if fields.get("name") != SKILL_NAME:
                errors.append("SKILL.md name must be " + SKILL_NAME)
            if not fields.get("description") or fields.get("description") in ("|", ">"):
                errors.append("SKILL.md needs a nonempty scalar description")
            if declared_version != version or declared_version is None:
                errors.append("SKILL.md metadata.version must match VERSION")
        except ValueError as error:
            errors.append(str(error))
    try:
        files = project_files(root)
    except ValueError as error:
        errors.append(str(error))
        files = []
    for path in files:
        if path.suffix not in TEXT_SUFFIXES and path.name not in ("LICENSE", "VERSION"):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append("Expected UTF-8 text: " + relative)
            continue
        for match in PRIVATE_PATH.finditer(text):
            if match.group(1).lower() not in GENERIC_USERS and not match.group(1).startswith(("$", "{")):
                errors.append("Machine-specific home path in " + relative)
                break
        # Source code can intentionally contain scanner patterns and test fixtures.
        if path.suffix in (".md", ".yaml", ".yml") and UNFINISHED.search(without_fences(text)):
            errors.append("Unfinished scaffold marker in " + relative)
        if path.suffix != ".md":
            continue
        for target in markdown_targets(text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            local = unquote(parsed.path)
            resolved = (root / local.lstrip("/") if local.startswith("/") else path.parent / local).resolve()
            try:
                rel_target = resolved.relative_to(root)
            except ValueError:
                errors.append("Local link leaves repository in " + relative + ": " + target)
                continue
            if any(part in IGNORED_PARTS for part in rel_target.parts) or not resolved.exists():
                errors.append("Unresolved local link in " + relative + ": " + target)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = validate_project(args.root)
    print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
