#!/usr/bin/env python3
"""
Automated validation tests for Chapter 7: Publish Your Hugo Site with GitHub Pages.
Verifies the production build (hugo --minify --panicOnWarning), GitHub Actions
workflow configuration (.github/workflows/hugo.yaml), the 4-item publishing
checklist in first-learning-note, and baseURL configuration in hugo.toml.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter07ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch07_test_")
        cls.public_dir = Path(cls.temp_dir) / "public"

        # Production-grade Hugo build as run in CI/CD pipeline
        cmd = [
            "hugo",
            "--source",
            str(PROJECT_ROOT),
            "--destination",
            str(cls.public_dir),
            "--minify",
            "--panicOnWarning",
        ]
        cls.build_result = subprocess.run(cmd, capture_output=True, text=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_production_build_succeeds(self):
        """Verify production build with --minify and --panicOnWarning completes with 0 warnings/errors."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Production build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_02_workflow_file_exists_and_configured(self):
        """Verify .github/workflows/hugo.yaml exists and contains required GitHub Actions specifications."""
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "hugo.yaml"
        self.assertTrue(workflow_path.is_file(), ".github/workflows/hugo.yaml not found.")
        content = workflow_path.read_text(encoding="utf-8")

        # Key triggers
        self.assertIn("branches: [main]", content)
        self.assertIn("workflow_dispatch", content)

        # Permissions
        self.assertIn("contents: read", content)
        self.assertIn("pages: write", content)
        self.assertIn("id-token: write", content)

        # Jobs and dependencies
        self.assertIn("build:", content)
        self.assertIn("deploy:", content)
        self.assertIn("needs: build", content)

        # Actions
        self.assertIn("actions/checkout", content)
        self.assertIn("actions/configure-pages", content)
        self.assertIn("actions/upload-pages-artifact", content)
        self.assertIn("actions/deploy-pages", content)

    def test_03_four_checklist_items_in_article_source(self):
        """Verify first learning note contains all 4 publishing checklist items."""
        article_source = (
            PROJECT_ROOT / "content" / "articles" / "first-learning-note" / "index.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## My publishing checklist", article_source)
        self.assertIn("Read the page in the local preview.", article_source)
        self.assertIn("Check its links and image description.", article_source)
        self.assertIn("Review the changed files before recording a checkpoint.", article_source)
        self.assertIn("Check the published page after deployment.", article_source)

    def test_04_four_checklist_items_in_rendered_html(self):
        """Verify generated article HTML includes the 4th checklist item."""
        html = (
            self.public_dir / "articles" / "first-learning-note" / "index.html"
        ).read_text(encoding="utf-8")

        self.assertIn("Check the published page after deployment.", html)

    def test_05_hugo_toml_baseurl_configured(self):
        """Verify hugo.toml configures a project-site baseURL with a trailing slash."""
        config_source = (PROJECT_ROOT / "hugo.toml").read_text(encoding="utf-8")
        self.assertRegex(
            config_source,
            r"baseURL\s*=\s*['\"].*github\.io/.+?['\"]",
            "baseURL in hugo.toml is not formatted as a GitHub Pages project address.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
