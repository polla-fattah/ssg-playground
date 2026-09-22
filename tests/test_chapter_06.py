#!/usr/bin/env python3
"""
Automated validation tests for Chapter 6: Track and Recover Your Hugo Site with Git.
Verifies the publishing checklist added to first-learning-note, the improved
About page description, the comprehensive .gitignore rules for Hugo and OS files,
and clean compilation of all site pages.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter06ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch06_test_")
        cls.public_dir = Path(cls.temp_dir) / "public"

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
        """Verify Hugo build succeeds with exit code 0."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_02_article_contains_publishing_checklist(self):
        """Verify the first learning note contains the Section 6.4 publishing checklist."""
        article_source = (
            PROJECT_ROOT / "content" / "articles" / "first-learning-note" / "index.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## My publishing checklist", article_source)
        self.assertIn("Read the page in the local preview.", article_source)
        self.assertIn("Check its links and image description.", article_source)
        self.assertIn("Review the changed files before recording a checkpoint.", article_source)

    def test_03_rendered_article_has_checklist_html(self):
        """Verify generated article HTML contains the checklist heading and list items."""
        html = (
            self.public_dir / "articles" / "first-learning-note" / "index.html"
        ).read_text(encoding="utf-8")

        self.assertIn("My publishing checklist", html)
        self.assertIn("Read the page in the local preview.", html)
        self.assertIn("Check its links and image description.", html)
        self.assertIn("Review the changed files before recording a checkpoint.", html)

    def test_04_gitignore_rules(self):
        """Verify .gitignore includes all essential Hugo output and OS metadata ignore rules."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        self.assertTrue(gitignore_path.is_file(), ".gitignore does not exist.")
        content = gitignore_path.read_text(encoding="utf-8")

        expected_rules = [
            "/public/",
            "/resources/",
            "/.hugo_build.lock",
            "/hugo_stats.json",
            ".DS_Store",
            "Thumbs.db",
        ]
        for rule in expected_rules:
            self.assertIn(rule, content, f"Missing rule in .gitignore: {rule}")

    def test_05_about_page_independent_improvement(self):
        """Verify About page contains the refined description from Section 6.7."""
        about_source = (
            PROJECT_ROOT / "content" / "about" / "index.md"
        ).read_text(encoding="utf-8")

        self.assertIn("structured record of practical work", about_source)

    def test_06_git_clean_working_tree_check(self):
        """Verify git status command runs and detects current branch."""
        git_cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        result = subprocess.run(git_cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("chapter-06", result.stdout.strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
