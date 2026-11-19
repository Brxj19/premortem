"""Smoke test: repo structure, fixtures and answer key are intact."""
import json
import subprocess
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
        "fixtures/answer-key.json",
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


class TestPyShopFixture(unittest.TestCase):

    FIXTURE_DIR = ROOT / "fixtures" / "py-shop"

    def test_py_files_exist(self):
        expected = [
            "app/__init__.py", "app/main.py", "app/routes.py", "app/pay.py",
            "app/refund.py", "app/products.py", "app/upload.py",
            "app/email_service.py", "app/jobs.py", "app/models.py",
            "app/db.py", "app/settings.py", "app/shipping.py",
            "app/inventory.py", "app/auth.py",
        ]
        for f in expected:
            with self.subTest(file=f):
                self.assertTrue(
                    (self.FIXTURE_DIR / f).is_file(), f"Missing: {f}"
                )

    def test_py_files_compile(self):
        for py_file in self.FIXTURE_DIR.rglob("*.py"):
            with self.subTest(file=str(py_file.relative_to(ROOT))):
                result = subprocess.run(
                    ["python3", "-m", "py_compile", str(py_file)],
                    capture_output=True, text=True,
                )
                self.assertEqual(
                    result.returncode, 0,
                    f"Compile error in {py_file.name}: {result.stderr}",
                )


class TestTsShopFixture(unittest.TestCase):

    FIXTURE_DIR = ROOT / "fixtures" / "ts-shop"

    def test_ts_files_exist(self):
        expected = [
            "src/app.ts", "src/config.ts", "src/db.ts", "src/auth.ts",
            "src/services/payment.ts", "src/services/refund.ts",
            "src/services/products.ts", "src/services/upload.ts",
            "src/services/email.ts", "src/services/jobs.ts",
            "src/services/shipping.ts", "src/services/inventory.ts",
            "src/routes/checkout.ts", "src/routes/refund.ts",
            "src/routes/products.ts", "src/routes/upload.ts",
            "src/routes/shipping.ts", "src/routes/admin.ts",
            "app/api/admin/products/route.ts",
        ]
        for f in expected:
            with self.subTest(file=f):
                self.assertTrue(
                    (self.FIXTURE_DIR / f).is_file(), f"Missing: {f}"
                )

    def test_ts_files_compile(self):
        tsconfig = self.FIXTURE_DIR / "tsconfig.json"
        if not tsconfig.exists():
            self.skipTest("tsconfig.json not found")
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "-p", str(tsconfig)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(
            result.returncode, 0,
            f"TypeScript compile errors:\n{result.stdout}",
        )


class TestAnswerKey(unittest.TestCase):

    def setUp(self):
        with open(ROOT / "fixtures" / "answer-key.json") as f:
            self.data = json.load(f)

    def test_schema_version(self):
        self.assertEqual(self.data["schema_version"], "1")

    def test_both_fixtures_present(self):
        names = [f["fixture"] for f in self.data["fixtures"]]
        self.assertIn("py-shop", names)
        self.assertIn("ts-shop", names)

    def test_expected_count(self):
        for fixture in self.data["fixtures"]:
            with self.subTest(fixture=fixture["fixture"]):
                self.assertGreaterEqual(len(fixture["expected"]), 12)

    def test_controls_present(self):
        for fixture in self.data["fixtures"]:
            with self.subTest(fixture=fixture["fixture"]):
                self.assertGreaterEqual(len(fixture["controls"]), 4)

    def test_silent_handlers_present(self):
        for fixture in self.data["fixtures"]:
            with self.subTest(fixture=fixture["fixture"]):
                self.assertGreaterEqual(len(fixture["silent_handlers"]), 2)

    def test_expected_fields(self):
        required = {"file", "function", "entity_type", "mode", "status"}
        for fixture in self.data["fixtures"]:
            for exp in fixture["expected"]:
                with self.subTest(fixture=fixture["fixture"], planted=exp.get("planted")):
                    self.assertTrue(
                        required.issubset(exp.keys()),
                        f"Missing fields: {required - exp.keys()}",
                    )

    def test_all_12_planted_bugs_per_fixture(self):
        for fixture in self.data["fixtures"]:
            planted_ids = {e["planted"] for e in fixture["expected"]}
            for i in range(1, 13):
                with self.subTest(fixture=fixture["fixture"], planted=i):
                    self.assertIn(i, planted_ids, f"Missing planted bug #{i}")


if __name__ == "__main__":
    unittest.main()
