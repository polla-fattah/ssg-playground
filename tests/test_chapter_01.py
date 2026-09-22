#!/usr/bin/env python3
"""
Automated validation tests for Chapter 1: Your First Hugo Website.
Verifies Hugo installation, build integrity, generated HTML content,
navigation anchor targets, and static assets.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter01ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch01_test_")
        cls.public_dir = Path(cls.temp_dir) / "public"

        # Run hugo build outputting to temporary directory
        cmd = [
            "hugo",
            "--source",
            str(PROJECT_ROOT),
            "--destination",
            str(cls.public_dir),
            "--printPathWarnings",
        ]
        cls.build_result = subprocess.run(cmd, capture_output=True, text=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_hugo_is_installed_and_meets_version_requirement(self):
        """Verify that Hugo is installed and is version 0.146.0 or newer."""
        res = subprocess.run(["hugo", "version"], capture_output=True, text=True)
        self.assertEqual(
            res.returncode,
            0,
            "Hugo is not recognized or not found in system PATH.",
        )
        match = re.search(r"v?(\d+)\.(\d+)\.(\d+)", res.stdout)
        self.assertIsNotNone(match, f"Unable to parse Hugo version from: {res.stdout}")
        major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
        # Expect version >= 0.146.0
        self.assertTrue(
            (major > 0) or (major == 0 and minor >= 146),
            f"Hugo version must be at least 0.146.0 (found {major}.{minor}.{patch})",
        )

    def test_02_hugo_build_succeeds(self):
        """Verify that the project builds cleanly without errors."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Hugo build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_03_index_html_exists(self):
        """Verify that index.html is generated at the website root."""
        index_file = self.public_dir / "index.html"
        self.assertTrue(index_file.is_file(), "index.html was not generated.")

    def test_04_html_contains_required_structure_and_title(self):
        """Verify title, site name, and h1 heading in rendered HTML."""
        index_file = self.public_dir / "index.html"
        content = index_file.read_text(encoding="utf-8")

        self.assertIn("My Knowledge Notebook", content, "Site title missing from output.")
        self.assertIn("<h1", content, "Main <h1> heading missing from output.")
        self.assertIn("Dana", content, "Starter author name missing from body text.")

    def test_05_navigation_anchors_and_targets_exist(self):
        """Verify navigation links point to valid in-page section identifiers."""
        index_file = self.public_dir / "index.html"
        content = index_file.read_text(encoding="utf-8")

        # Links in navigation
        self.assertIn("#my-interests", content, "Navigation link to #my-interests missing.")
        self.assertIn("#next-steps", content, "Navigation link to #next-steps missing.")

        # Destination IDs in rendered HTML headings
        self.assertTrue(
            re.search(r'id=["\']my-interests["\']', content),
            "Heading with id='my-interests' not found in generated HTML.",
        )
        self.assertTrue(
            re.search(r'id=["\']next-steps["\']', content),
            "Heading with id='next-steps' not found in generated HTML.",
        )

    def test_06_css_stylesheet_is_copied_and_linked(self):
        """Verify that site.css is compiled/copied and linked in index.html."""
        index_file = self.public_dir / "index.html"
        content = index_file.read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\'][^"\']*site\.css["\']', content),
            "Stylesheet link tag for site.css missing from index.html.",
        )

        css_file = self.public_dir / "css" / "site.css"
        self.assertTrue(css_file.is_file(), "static/css/site.css was not copied to public/css/site.css.")
        css_content = css_file.read_text(encoding="utf-8")
        self.assertIn("box-sizing", css_content, "CSS content appears corrupted or empty.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
