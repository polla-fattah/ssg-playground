#!/usr/bin/env python3
"""
Automated validation tests for Chapter 8: Work with an AI Agent on Your Hugo Site.
Verifies project guidance in AGENTS.md, bounded content additions in content/resources/index.md,
exact bullet count and word limits, internal relative link integrity, and ensures AGENTS.md
is not published as an authored site page.
"""

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Chapter08ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp(prefix="ssg_ch08_test_")
        cls.public_dir = Path(cls.temp_dir) / "public"

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

    def test_02_agents_md_exists_and_configured(self):
        """Verify AGENTS.md exists at project root with required sections and safety agreements."""
        agents_file = PROJECT_ROOT / "AGENTS.md"
        self.assertTrue(agents_file.is_file(), "AGENTS.md not found at project root.")
        content = agents_file.read_text(encoding="utf-8")

        self.assertIn("# Project guidance", content)
        self.assertIn("## Files", content)
        self.assertIn("## Working agreements", content)
        self.assertIn("Do not invent experiences", content)
        self.assertIn("Do not edit generated public/ or resources/ files by hand.", content)
        self.assertIn("Leave staging, committing, pushing, and deployment to the reader", content)

    def test_03_agents_md_not_published_as_html_page(self):
        """Verify AGENTS.md is not rendered as a website page in public/."""
        rendered_agents = self.public_dir / "agents" / "index.html"
        self.assertFalse(rendered_agents.exists(), "AGENTS.md was erroneously rendered as a public web page.")

    def test_04_resources_new_section_structure(self):
        """Verify content/resources/index.md contains the exact 3-bullet 'How to use these resources' section."""
        resources_source = (PROJECT_ROOT / "content" / "resources" / "index.md").read_text(encoding="utf-8")

        self.assertIn("## How to use these resources", resources_source)

        # Extract the section text between '## How to use these resources' and next heading
        section_match = re.search(
            r"## How to use these resources\s*\n(.*?)\n##\s+",
            resources_source,
            re.DOTALL,
        )
        self.assertIsNotNone(section_match, "Could not isolate 'How to use these resources' section.")
        section_text = section_match.group(1).strip()

        # Check bullets count
        bullets = [line for line in section_text.splitlines() if line.strip().startswith("-")]
        self.assertEqual(len(bullets), 3, f"Expected exactly 3 bullets, found {len(bullets)}.")

        # Check word limit (under 70 words)
        words = section_text.split()
        self.assertLessEqual(
            len(words),
            70,
            f"Section exceeded 70 words limit: {len(words)} words found.",
        )

        # Check link destinations
        self.assertIn("https://gohugo.io/documentation/", section_text)
        self.assertIn("../articles/first-learning-note/", section_text)
        self.assertIn("../projects/learning-notebook/", section_text)

    def test_05_preserved_existing_sections_in_resources(self):
        """Verify original sections in content/resources/index.md or rendered HTML were preserved."""
        resources_source = (PROJECT_ROOT / "content" / "resources" / "index.md").read_text(encoding="utf-8")
        html = (self.public_dir / "resources" / "index.html").read_text(encoding="utf-8")
        
        # In chapter 08 it was markdown; in chapter 12+ it is rendered via JSON partial
        has_web_pub = ("## Website publishing" in resources_source) or ("website-publishing" in html)
        self.assertTrue(has_web_pub, "Website publishing section missing")
        self.assertIn("## Examples from this notebook", resources_source)

    def test_06_rendered_html_contains_new_resources_section(self):
        """Verify rendered HTML in public/resources/index.html includes the new section and valid links."""
        html = (self.public_dir / "resources" / "index.html").read_text(encoding="utf-8")
        self.assertIn("How to use these resources", html)
        self.assertIn("../articles/first-learning-note/", html)
        self.assertIn("../projects/learning-notebook/", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
