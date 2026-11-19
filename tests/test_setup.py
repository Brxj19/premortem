"""Smoke test: repo structure and fixtures are intact."""
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestRepoStructure(unittest.TestCase):

    REQUIRED_DIRS = [
        "pack/shared/catalog",
        "pack/shared/scripts/lib",
        "pack/skills/premortem-scan",
        "pack/skills/premortem-query",
        "pack/skills/premortem-pr",
        "pack/skills/premortem-harden",
        "pack/skills/premortem-design",
        "fixtures/py-shop",
        "fixtures/ts-shop",
        "tests",
        "tools",
    ]

    REQUIRED_FILES = [
        "pack/VERSION",
        "pack/README.md",
        "pack/shared/schema.md",
        "pack/shared/scoring.md",
        "pack/shared/resilience.md",
        "Makefile",
        "DECISIONS.md",
    ]

    def test_directories_exist(self):
        for d in self.REQUIRED_DIRS:
            with self.subTest(directory=d):
                self.assertTrue((ROOT / d).is_dir(), f"Missing directory: {d}")

    def test_files_exist(self):
        for f in self.REQUIRED_FILES:
            with self.subTest(file=f):
                self.assertTrue((ROOT / f).is_file(), f"Missing file: {f}")

    def test_version_file(self):
        version = (ROOT / "pack/VERSION").read_text().strip()
        parts = version.split(".")
        self.assertEqual(len(parts), 3, f"VERSION must be semver, got: {version}")
        for part in parts:
            self.assertTrue(part.isdigit(), f"Non-numeric version part: {part}")


if __name__ == "__main__":
    unittest.main()
