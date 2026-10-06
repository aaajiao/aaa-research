"""Offline release lifecycle tests; no calls to AAA or GitHub."""

import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_release import build_release, payload_files, verify_archive
from validate_project import REQUIRED_FILES, validate_project


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="aaa-release-tests-")
        self.root = (Path(self.temporary.name) / "project").resolve()
        self.root.mkdir()
        for name in REQUIRED_FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Release fixture.\n", encoding="utf-8")
        self.write("VERSION", "1.0.0\n")
        self.write("SKILL.md", "---\nname: aaa-research\ndescription: Research AAA sources.\n"
                   "metadata:\n  version: \"1.0.0\"\n---\n\n"
                   "# Research\n\n[Access](references/access.md)\n")
        self.write("references/access.md", "# Access\n\n[Probe](../scripts/access_probe.py)\n")
        self.write("agents/openai.yaml", 'interface:\n  display_name: "AAA Research"\n')
        self.write("scripts/access_probe.py", 'print("fixture runtime")\n')
        self.write("tests/test_access_probe.py", '# Included runtime regression suite.\n')
        self.write("README.md", "# Project\n\n[Validation](docs/VALIDATION.md)\n")
        self.write("docs/VALIDATION.md", "# Validation\n\n[Project](../README.md)\n")

    def tearDown(self):
        self.temporary.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_complete_release_extracts_with_checksums_and_only_runtime_files(self):
        for name in ("scripts/build_release.py", "tests/test_release.py", "docs/private.pdf",
                     "work/source.pdf", ".git/config", "dist/old.zip", ".venv/cache.bin",
                     "scripts/__pycache__/cache.pyc"):
            self.write(name, "excluded fixture\n")
        self.assertEqual(validate_project(self.root), [])
        result = build_release(self.root)
        archive = Path(result["archive"])
        self.assertEqual(archive.name, "aaa-research-v1.0.0.zip")
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(result["sha256"], digest)
        self.assertEqual(Path(result["checksum_file"]).read_text(), digest + "  " + archive.name + "\n")
        expected = {
            "SKILL.md", "VERSION", "LICENSE", "NOTICE.md", "agents/openai.yaml",
            "references/access.md", "scripts/access_probe.py", "tests/test_access_probe.py",
        }
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(set(bundle.namelist()), {"aaa-research/" + name for name in expected})
            target = Path(self.temporary.name) / "installed"
            bundle.extractall(target)
        for name in expected:
            self.assertEqual((target / "aaa-research" / name).read_bytes(), (self.root / name).read_bytes())

    def test_rebuild_is_identical_despite_source_modes_and_timestamps(self):
        one = build_release(self.root, Path(self.temporary.name) / "one")
        for path in payload_files(self.root):
            os.utime(path, (1700000000, 1700000000))
            path.chmod(0o700)
        two = build_release(self.root, Path(self.temporary.name) / "two")
        self.assertEqual(Path(one["archive"]).read_bytes(), Path(two["archive"]).read_bytes())
        self.assertEqual(Path(one["checksum_file"]).read_bytes(), Path(two["checksum_file"]).read_bytes())

    def test_version_mismatch_and_missing_required_documents_block_build(self):
        self.write("VERSION", "1.1.0\n")
        self.assertTrue(any("metadata.version" in error for error in validate_project(self.root)))
        with self.assertRaises(ValueError):
            build_release(self.root)
        self.write("VERSION", "1.0.0\n")
        (self.root / "README.zh-CN.md").unlink()
        self.assertTrue(any("README.zh-CN.md" in error for error in validate_project(self.root)))

    def test_local_links_resolve_from_root_and_nested_docs(self):
        self.assertEqual(validate_project(self.root), [])
        self.write("docs/VALIDATION.md", "[Missing](../missing.md)\n")
        self.assertTrue(any("Unresolved local link" in error for error in validate_project(self.root)))
        self.write("docs/VALIDATION.md", "[Outside](../../secret.md)\n")
        self.assertTrue(any("leaves repository" in error for error in validate_project(self.root)))

    def test_payload_cannot_link_to_a_repository_only_document(self):
        self.write("references/access.md", "[Repository docs](../docs/VALIDATION.md)\n")
        self.assertEqual(validate_project(self.root), [])
        with self.assertRaisesRegex(ValueError, "excluded file"):
            build_release(self.root)

    def test_real_private_paths_and_scaffolding_fail_but_example_commands_pass(self):
        self.write("README.md", "Example command:\n\n```bash\npython3 /path/to/aaa-research/scripts/access_probe.py 'PUBLIC_RECORD_URL'\n```\n")
        self.assertEqual(validate_project(self.root), [])
        self.write("README.md", "Machine file: /" + "Users/real-person/private/source.pdf\n")
        self.assertTrue(any("home path" in error for error in validate_project(self.root)))
        self.write("README.md", "TODO: finish installation instructions\n")
        self.assertTrue(any("scaffold" in error for error in validate_project(self.root)))

    def test_symlinked_payload_and_unexpected_media_are_rejected(self):
        external = Path(self.temporary.name) / "outside.txt"
        external.write_text("Not authorized for the package.\n")
        try:
            (self.root / "references/leak.md").symlink_to(external)
        except OSError:
            self.skipTest("Host cannot create symlinks")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            build_release(self.root)
        (self.root / "references/leak.md").unlink()
        self.write("references/source.pdf", "not part of the skill\n")
        with self.assertRaisesRegex(ValueError, "Unexpected payload"):
            build_release(self.root)

    def test_archive_verification_detects_changed_content(self):
        result = build_release(self.root)
        payload = {path.relative_to(self.root).as_posix(): path.read_bytes() for path in payload_files(self.root)}
        damaged = Path(self.temporary.name) / "changed.zip"
        with zipfile.ZipFile(result["archive"]) as source, zipfile.ZipFile(damaged, "w") as target:
            for info in source.infolist():
                data = source.read(info.filename)
                if info.filename.endswith("/VERSION"):
                    data = b"9.9.9\n"
                target.writestr(info, data)
        with self.assertRaisesRegex(ValueError, "content hash mismatch"):
            verify_archive(damaged, payload)


if __name__ == "__main__":
    unittest.main(verbosity=2)
