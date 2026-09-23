import os
import re
import subprocess
import unittest
import yaml

class TestChapter18(unittest.TestCase):
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
        """Hugo build should succeed with minification and panicOnWarning."""
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

    def test_02_workflow_version_check_step(self):
        """checks.yaml must contain step comparing HUGO_VERSION between hugo.yaml and checks.yaml."""
        checks_path = os.path.join(self.repo_root, ".github", "workflows", "checks.yaml")
        hugo_path = os.path.join(self.repo_root, ".github", "workflows", "hugo.yaml")

        self.assertTrue(os.path.exists(checks_path))
        self.assertTrue(os.path.exists(hugo_path))

        with open(checks_path, "r", encoding="utf-8") as f:
            checks_wf = f.read()
        with open(hugo_path, "r", encoding="utf-8") as f:
            hugo_wf = f.read()

        # Check step existence in checks.yaml
        self.assertIn("Check that both workflows pin the same Hugo version", checks_wf)
        self.assertIn("grep 'HUGO_VERSION:' .github/workflows/hugo.yaml", checks_wf)
        self.assertIn("grep 'HUGO_VERSION:' .github/workflows/checks.yaml", checks_wf)

        # Check actual values match
        hugo_ver_match = re.search(r'HUGO_VERSION:\s*["\']?([^"\'\s]+)["\']?', hugo_wf)
        checks_ver_match = re.search(r'HUGO_VERSION:\s*["\']?([^"\'\s]+)["\']?', checks_wf)
        self.assertIsNotNone(hugo_ver_match)
        self.assertIsNotNone(checks_ver_match)
        self.assertEqual(
            hugo_ver_match.group(1),
            checks_ver_match.group(1),
            "HUGO_VERSION in hugo.yaml and checks.yaml do not match!"
        )

    def test_03_reading_list_archived_content(self):
        """content/projects/reading-list/index.md must have status: 'archived', draft: false, and notice."""
        rl_path = os.path.join(self.repo_root, "content", "projects", "reading-list", "index.md")
        self.assertTrue(os.path.exists(rl_path))

        with open(rl_path, "r", encoding="utf-8") as f:
            text = f.read()

        parts = text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Invalid front matter separation")
        fm = yaml.safe_load(parts[1])

        self.assertEqual(fm.get("draft"), False)
        self.assertEqual(fm.get("params", {}).get("status"), "archived")

        body = parts[2]
        self.assertIn("**Archived.**", body)
        self.assertIn("The resource directory on the [Resources page](../../resources/) now does this job", body)

    def test_04_rendered_project_list_shows_archived(self):
        """public/projects/index.html must display reading-list as archived without breaking links."""
        projects_html_path = os.path.join(self.public_dir, "projects", "index.html")
        rl_html_path = os.path.join(self.public_dir, "projects", "reading-list", "index.html")

        self.assertTrue(os.path.exists(projects_html_path))
        self.assertTrue(os.path.exists(rl_html_path), "Archived project page should still exist at its address")

        with open(projects_html_path, "r", encoding="utf-8") as f:
            proj_html = f.read()

        self.assertIn("My website reading list", proj_html)
        self.assertIn("archived", proj_html)

        with open(rl_html_path, "r", encoding="utf-8") as f:
            rl_html = f.read()

        self.assertIn("archived", rl_html)
        self.assertIn("The resource directory on the", rl_html)

    def test_05_maintenance_md_file(self):
        """MAINTENANCE.md must exist and outline the regular maintenance routine and decisions."""
        maint_path = os.path.join(self.repo_root, "MAINTENANCE.md")
        self.assertTrue(os.path.exists(maint_path), "MAINTENANCE.md missing")

        with open(maint_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("# Maintenance routine", content)
        self.assertIn("## Every few months", content)
        self.assertIn("source_checked", content)
        self.assertIn("## When a dependency changes", content)
        self.assertIn("HUGO_VERSION", content)
        self.assertIn("## After any mistake reaches the live site", content)
        self.assertIn("git revert", content)
        self.assertIn("## Decisions to keep", content)
        self.assertIn("archived", content)

    def test_06_agents_guidance_updated(self):
        """AGENTS.md must list MAINTENANCE.md and include the archiving agreement."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        self.assertTrue(os.path.exists(agents_path))

        with open(agents_path, "r", encoding="utf-8") as f:
            agents_text = f.read()

        self.assertIn("The maintenance routine is in MAINTENANCE.md.", agents_text)
        self.assertIn("Archiving a page means changing its status and saying so in the body", agents_text)
        self.assertIn("It does not mean setting draft: true", agents_text)

if __name__ == "__main__":
    unittest.main()
