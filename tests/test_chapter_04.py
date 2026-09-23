#!/usr/bin/env python3
"""
Automated validation tests for Chapter 4: Understand the HTML Behind Your Pages.
Verifies semantic HTML structure, shared layout footer updates, skip-link
target integrity, single h1 per page, valid attributes (src, alt, id, class),
and character entity handling.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter04ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch04_test_")
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
        """Verify Hugo build succeeds with return code 0."""
        self.assertEqual(
            self.build_result.returncode,
            0,
            f"Build failed.\nSTDOUT:\n{self.build_result.stdout}\nSTDERR:\n{self.build_result.stderr}",
        )

    def test_02_layout_source_footer(self):
        """Verify layout files contain updated persistent footer structure."""
        layout_path = PROJECT_ROOT / "layouts" / "all.html"
        footer_partial = PROJECT_ROOT / "layouts" / "_partials" / "footer.html"
        self.assertTrue(layout_path.is_file(), "layouts/all.html not found.")

        if footer_partial.is_file():
            content = footer_partial.read_text(encoding="utf-8")
        else:
            content = layout_path.read_text(encoding="utf-8")

        self.assertIn("<footer>", content)
        self.assertIn("<p>Learn, review &amp; share.</p>", content)
        self.assertTrue(
            'href="{{ "about/" | relLangURL }}"' in content
            or 'href="{{ "about/" | relURL }}"' in content
        )

    def test_03_all_pages_have_updated_footer(self):
        """Verify every generated HTML page displays the new structured footer."""
        pages = [p for p in self.public_dir.glob("**/*.html") if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(pages), 7, f"Expected at least 7 pages, found {len(pages)}")

        for page in pages:
            html = page.read_text(encoding="utf-8")
            self.assertIn("<footer>", html, f"Missing <footer> in {page.name}")
            self.assertIn("Learn, review &amp; share.", html, f"Missing footer primary text in {page.name}")
            self.assertIn('class="footer-note"', html, f"Missing footer-note class in {page.name}")
            self.assertRegex(
                html,
                r'<a[^>]+href="[^"]*about/?"[^>]*>about this notebook</a>',
                f"Missing or malformed About link in footer of {page.name}",
            )

    def test_04_skip_link_and_target_integrity(self):
        """Verify skip-link href matches target element id on every page."""
        pages = [p for p in self.public_dir.glob("**/*.html") if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8")]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            # Verify skip link exists
            self.assertIn(
                'href="#main"',
                html,
                f"Missing skip link href='#main' on {page.relative_to(self.public_dir)}",
            )
            # Verify target element exists with matching id and tabindex="-1"
            self.assertRegex(
                html,
                r'<main[^>]+id="main"[^>]+tabindex="-1"',
                f"Missing <main id='main' tabindex='-1'> target on {page.relative_to(self.public_dir)}",
            )

    def test_05_single_h1_per_page(self):
        """Verify each page has exactly one h1 element for clean semantic outline."""
        pages = [p for p in self.public_dir.glob("**/*.html") if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8")]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            h1_matches = re.findall(r"<h1[^>]*>.*?</h1>", html, re.DOTALL | re.IGNORECASE)
            self.assertEqual(
                len(h1_matches),
                1,
                f"Page {page.relative_to(self.public_dir)} has {len(h1_matches)} <h1> elements; expected exactly 1.",
            )

    def test_06_semantic_landmarks_present(self):
        """Verify standard semantic elements (header, nav, main, article, footer) exist."""
        pages = [p for p in self.public_dir.glob("**/*.html") if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8")]
        landmarks = ["<header", "<nav", "<main", "<article", "<footer"]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            for landmark in landmarks:
                self.assertIn(
                    landmark,
                    html,
                    f"Landmark {landmark}> missing on {page.relative_to(self.public_dir)}",
                )

    def test_07_article_image_attributes_and_void_elements(self):
        """Verify article image has valid src and non-empty alt, and no void closing tags."""
        article_page = self.public_dir / "articles" / "first-learning-note" / "index.html"
        self.assertTrue(article_page.is_file())
        html = article_page.read_text(encoding="utf-8")

        # Check image attributes
        img_match = re.search(r'<img\s+([^>]+)>', html)
        self.assertIsNotNone(img_match, "Article page missing <img> element.")
        attrs = img_match.group(1)
        self.assertIn("notebook-preview.png", attrs)
        self.assertIn('alt="', attrs)
        # Ensure alt is not empty
        self.assertNotRegex(attrs, r'alt=""')

        # Check no invalid closing tag </img>
        self.assertNotIn("</img>", html, "Invalid </img> closing tag found.")
        self.assertNotIn("</meta>", html, "Invalid </meta> closing tag found.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
