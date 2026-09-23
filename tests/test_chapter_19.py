import os
import subprocess
import unittest

class TestChapter19(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.public_dir = os.path.join(cls.repo_root, "public")
        # Ensure fresh build
        result = subprocess.run(
            ["hugo", "--minify", "--panicOnWarning"],
            cwd=cls.repo_root,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Hugo build failed:\n{result.stderr}"

    def test_01_hugo_build_clean(self):
        """Hugo build should succeed with minification and panicOnWarning across both languages."""
        result = subprocess.run(
            ["hugo", "--minify", "--panicOnWarning"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.returncode, 0,
            f"Hugo build failed:\nStdout: {result.stdout}\nStderr: {result.stderr}"
        )

    def test_02_brief_file_structure(self):
        """BRIEF.md must exist at project root and contain all required sections."""
        brief_path = os.path.join(self.repo_root, "BRIEF.md")
        self.assertTrue(os.path.exists(brief_path), "BRIEF.md is missing at project root")

        with open(brief_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_sections = [
            "## Audience",
            "## Purpose",
            "## Success",
            "## Content",
            "## Out of scope",
            "## Capabilities",
            "## Review and Maintenance",
        ]
        for section in required_sections:
            self.assertIn(section, content, f"Missing section '{section}' in BRIEF.md")

    def test_03_brief_capabilities_and_exclusions(self):
        """BRIEF.md must evaluate capabilities and define clear out-of-scope boundaries."""
        brief_path = os.path.join(self.repo_root, "BRIEF.md")
        with open(brief_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check that out of scope is explicit
        self.assertIn("Not a dynamic content management system", content)
        self.assertIn("No third-party analytics", content)

        # Check capabilities table evaluates yes, later, or no
        self.assertIn("Markdown pages & sections", content)
        self.assertIn("Checks on every proposal", content)
        self.assertIn("Maintenance routine", content)

    def test_04_agents_lists_brief(self):
        """AGENTS.md must list BRIEF.md under Files."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        self.assertTrue(os.path.exists(agents_path))

        with open(agents_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("The project brief is in BRIEF.md.", text)

    def test_05_maintenance_has_next_review_date(self):
        """MAINTENANCE.md must record next review date."""
        maint_path = os.path.join(self.repo_root, "MAINTENANCE.md")
        self.assertTrue(os.path.exists(maint_path))

        with open(maint_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("## Next review", text)
        self.assertIn("2026-", text)

if __name__ == "__main__":
    unittest.main()
