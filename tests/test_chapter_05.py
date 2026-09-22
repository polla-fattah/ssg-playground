#!/usr/bin/env python3
"""
Automated validation tests for Chapter 5: Practical CSS for Your Hugo Site.
Verifies the editable stylesheet in static/css/site.css, the published copy
in public/css/site.css, typography adjustments (body font-size: 1.125rem),
heading spacing (h2 margin-top: 2.5rem), the .footer-note styling rule,
and preservation of responsive/accessibility rules.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter05ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch05_test_")
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

    def test_02_stylesheet_copied_to_public(self):
        """Verify static/css/site.css is published directly to public/css/site.css."""
        static_css = PROJECT_ROOT / "static" / "css" / "site.css"
        public_css = self.public_dir / "css" / "site.css"
        self.assertTrue(static_css.is_file(), "static/css/site.css not found.")
        self.assertTrue(public_css.is_file(), "public/css/site.css not generated.")
        self.assertEqual(
            static_css.read_text(encoding="utf-8").strip(),
            public_css.read_text(encoding="utf-8").strip(),
            "Published CSS differs from source CSS in static/.",
        )

    def test_03_body_font_size_configured(self):
        """Verify body rule contains font-size: 1.125rem."""
        css = (PROJECT_ROOT / "static" / "css" / "site.css").read_text(encoding="utf-8")
        body_match = re.search(r"body\s*\{([^}]+)\}", css)
        self.assertIsNotNone(body_match, "body rule not found in site.css.")
        declarations = body_match.group(1)
        self.assertIn("font-size: 1.125rem;", declarations)
        self.assertIn("line-height: 1.7;", declarations)

    def test_04_h2_margin_top_increased(self):
        """Verify h2 heading has margin-top of 2.5rem (or >= 2.25rem)."""
        css = (PROJECT_ROOT / "static" / "css" / "site.css").read_text(encoding="utf-8")
        h2_match = re.search(r"\bh2\s*\{([^}]+)\}", css)
        self.assertIsNotNone(h2_match, "h2 rule not found in site.css.")
        declarations = h2_match.group(1)
        self.assertIn("margin-top: 2.5rem;", declarations)

    def test_05_footer_note_rule_exists(self):
        """Verify .footer-note rule has border, spacing, and quieter color."""
        css = (PROJECT_ROOT / "static" / "css" / "site.css").read_text(encoding="utf-8")
        fn_match = re.search(r"\.footer-note\s*\{([^}]+)\}", css)
        self.assertIsNotNone(fn_match, ".footer-note selector rule not found in site.css.")
        declarations = fn_match.group(1)
        self.assertIn("margin-top: 0.75rem;", declarations)
        self.assertIn("padding-top: 0.75rem;", declarations)
        self.assertIn("border-top: 1px solid #c5ccce;", declarations)
        self.assertIn("color: #46545b;", declarations)

    def test_06_responsive_and_accessible_rules_preserved(self):
        """Verify existing layout width, flexbox nav, focus, skip-link, and image rules are intact."""
        css = (PROJECT_ROOT / "static" / "css" / "site.css").read_text(encoding="utf-8")
        self.assertIn("width: min(100% - 2rem, 48rem);", css)
        self.assertIn("margin-inline: auto;", css)
        self.assertIn("display: flex;", css)
        self.assertIn("flex-wrap: wrap;", css)
        self.assertIn("gap: 1rem;", css)
        self.assertIn("a:focus-visible", css)
        self.assertIn(".skip-link", css)
        self.assertIn("max-width: 100%;", css)
        self.assertIn("overflow-x: auto;", css)

    def test_07_all_pages_reference_stylesheet(self):
        """Verify all generated HTML pages include link rel=stylesheet to css/site.css."""
        pages = list(self.public_dir.glob("**/*.html"))
        for page in pages:
            html = page.read_text(encoding="utf-8")
            self.assertRegex(
                html,
                r'<link[^>]+rel="stylesheet"[^>]+href="[^"]*css/site\.css"',
                f"Missing stylesheet link in {page.relative_to(self.public_dir)}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
