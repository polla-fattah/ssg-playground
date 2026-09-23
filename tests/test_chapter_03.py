#!/usr/bin/env python3
"""
Automated validation tests for Chapter 3: Organise a Useful Website.
Verifies all 7 site pages, section landing pages (_index.md),
leaf page bundles (index.md), shared navigation across every page,
and cross-section link integrity.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter03ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch03_test_")
        cls.public_dir = Path(cls.temp_dir) / "public"

        # Standard Hugo build
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

    def test_01_build_succeeds(self):
        """Verify Hugo build completes with exit code 0."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_02_all_seven_routes_exist(self):
        """Verify the 7 core pages exist in public directory."""
        expected_pages = [
            self.public_dir / "index.html",
            self.public_dir / "about" / "index.html",
            self.public_dir / "articles" / "index.html",
            self.public_dir / "articles" / "first-learning-note" / "index.html",
            self.public_dir / "projects" / "index.html",
            self.public_dir / "projects" / "learning-notebook" / "index.html",
            self.public_dir / "resources" / "index.html",
        ]
        for page in expected_pages:
            self.assertTrue(
                page.is_file(),
                f"Expected page missing: {page.relative_to(self.public_dir)}",
            )

    def test_03_shared_navigation_appears_on_every_page(self):
        """Verify shared 5-link navigation is present on every generated page."""
        nav_targets = ["about/", "articles/", "projects/", "resources/"]
        pages_to_check = [
            self.public_dir / "index.html",
            self.public_dir / "about" / "index.html",
            self.public_dir / "articles" / "index.html",
            self.public_dir / "articles" / "first-learning-note" / "index.html",
            self.public_dir / "projects" / "index.html",
            self.public_dir / "projects" / "learning-notebook" / "index.html",
            self.public_dir / "resources" / "index.html",
        ]
        for page in pages_to_check:
            content = page.read_text(encoding="utf-8")
            self.assertIn('<nav aria-label="Main navigation">', content, f"Nav missing on {page.name}")
            for target in nav_targets:
                self.assertIn(target, content, f"Link to {target} missing in navigation on {page.name}")

    def test_04_section_landing_pages_contain_manual_lists(self):
        """Verify Articles and Projects landing pages link to their child pages."""
        articles_html = (self.public_dir / "articles" / "index.html").read_text(encoding="utf-8")
        self.assertIn("first-learning-note/", articles_html, "Articles section does not link to first-learning-note.")

        projects_html = (self.public_dir / "projects" / "index.html").read_text(encoding="utf-8")
        self.assertIn("learning-notebook/", projects_html, "Projects section does not link to learning-notebook.")

    def test_05_cross_section_links(self):
        """Verify cross-section links on About, Project, and Resources pages."""
        about_html = (self.public_dir / "about" / "index.html").read_text(encoding="utf-8")
        self.assertTrue(
            "../articles/first-learning-note/" in about_html
            or "articles/first-learning-note/" in about_html
        )

        project_html = (self.public_dir / "projects" / "learning-notebook" / "index.html").read_text(encoding="utf-8")
        self.assertTrue(
            "../../articles/first-learning-note/" in project_html
            or "articles/first-learning-note/" in project_html
        )
        self.assertTrue(
            'href="../"' in project_html
            or 'href="/my-knowledge-site/"' in project_html
            or 'href="/my-knowledge-site/projects/"' in project_html,
            "Back to Projects link missing.",
        )

        resources_html = (self.public_dir / "resources" / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://gohugo.io/documentation/", resources_html)
        self.assertTrue(
            "../articles/first-learning-note/" in resources_html
            or "articles/first-learning-note/" in resources_html
        )
        self.assertTrue(
            "../projects/learning-notebook/" in resources_html
            or "projects/learning-notebook/" in resources_html
        )

    def test_06_home_page_explore_section(self):
        """Verify home page features 'Explore the notebook' section."""
        home_html = (self.public_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("Explore the notebook", home_html)
        self.assertIn("about/", home_html)
        self.assertIn("articles/", home_html)
        self.assertIn("projects/", home_html)
        self.assertIn("resources/", home_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
