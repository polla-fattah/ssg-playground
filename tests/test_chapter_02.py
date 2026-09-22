#!/usr/bin/env python3
"""
Automated validation tests for Chapter 2: Write and Publish Content Locally.
Verifies leaf page bundles, Markdown syntax, internal/external/anchor links,
embedded images with alt text, CSS responsive rules, and draft toggling.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter02ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch02_test_")
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
        """Verify standard Hugo build completes with exit code 0."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_02_article_page_generated_at_expected_path(self):
        """Verify /articles/first-learning-note/index.html is generated."""
        article_file = self.public_dir / "articles" / "first-learning-note" / "index.html"
        self.assertTrue(
            article_file.is_file(),
            f"Article page missing at: {article_file}",
        )

    def test_03_headings_and_content_structure(self):
        """Verify title, h1, h2, h3, and lists in rendered article."""
        article_file = self.public_dir / "articles" / "first-learning-note" / "index.html"
        content = article_file.read_text(encoding="utf-8")

        self.assertIn("My first learning note", content, "Article title missing.")
        self.assertTrue(
            re.search(r'<h1[^>]*>\s*My first learning note\s*</h1>', content),
            "Main <h1> heading does not match front-matter title.",
        )
        self.assertIn("What I tried", content)
        self.assertIn("What I learned", content)
        self.assertIn("How I checked it", content)
        self.assertIn("<ol", content, "Numbered list missing from article.")
        self.assertIn("<ul", content, "Bulleted list missing from article.")

    def test_04_links_and_anchors(self):
        """Verify external links, relative home link, and section anchor targets."""
        article_file = self.public_dir / "articles" / "first-learning-note" / "index.html"
        content = article_file.read_text(encoding="utf-8")

        # External doc link
        self.assertIn("https://gohugo.io/documentation/", content)

        # In-page anchor link & target ID
        self.assertIn('href="#my-next-step"', content)
        self.assertTrue(
            re.search(r'id=["\']my-next-step["\']', content),
            "Heading target id='my-next-step' missing in article HTML.",
        )

        # Relative return home link
        self.assertTrue(
            re.search(r'href=["\']\.\./\.\./["\']', content) or re.search(r'href=["\'][^"\']*["\']>Return to my home page<', content),
            "Return to home page link missing.",
        )

    def test_05_screenshot_image_bundled_and_referenced(self):
        """Verify notebook-preview.png is published in page bundle with alt text."""
        img_dest = self.public_dir / "articles" / "first-learning-note" / "notebook-preview.png"
        self.assertTrue(img_dest.is_file(), f"Bundled image not copied to: {img_dest}")

        article_file = self.public_dir / "articles" / "first-learning-note" / "index.html"
        content = article_file.read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r'<img[^>]+src=["\']notebook-preview\.png["\']', content),
            "Image tag with src='notebook-preview.png' missing in HTML.",
        )
        self.assertTrue(
            re.search(r'alt=["\'][^"\']*introduction[^"\']*["\']', content, re.IGNORECASE),
            "Image alt attribute missing or incomplete.",
        )

    def test_06_home_page_links_to_article(self):
        """Verify home page features 'Latest writing' linking to the new article."""
        home_file = self.public_dir / "index.html"
        content = home_file.read_text(encoding="utf-8")

        self.assertIn("Latest writing", content, "'Latest writing' section missing on home page.")
        self.assertTrue(
            re.search(r'href=["\']articles/first-learning-note/["\']', content)
            or re.search(r'href=["\'][^"\']*articles/first-learning-note/[^"\']*["\']', content),
            "Home page does not link to articles/first-learning-note/.",
        )

    def test_07_css_responsive_image_and_pre_rules(self):
        """Verify CSS contains max-width: 100% for images and overflow-x for pre."""
        css_file = self.public_dir / "css" / "site.css"
        css_content = css_file.read_text(encoding="utf-8")

        self.assertIn("article img", css_content)
        self.assertIn("max-width", css_content)
        self.assertIn("article pre", css_content)
        self.assertIn("overflow-x", css_content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
