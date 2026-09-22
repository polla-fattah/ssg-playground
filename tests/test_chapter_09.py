import os
import subprocess
import unittest
import yaml

class TestChapter09(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_hugo_build_clean(self):
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

    def test_archetype_exists_and_valid(self):
        """archetypes/projects.md must exist and contain the agreed content model starter."""
        archetype_path = os.path.join(self.repo_root, "archetypes", "projects.md")
        self.assertTrue(os.path.exists(archetype_path), "archetypes/projects.md does not exist")
        
        with open(archetype_path, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Front matter delimiter '---' missing in archetype")
        fm = yaml.safe_load(parts[1])
        
        self.assertIn("title", fm)
        self.assertIn("description", fm)
        self.assertTrue(fm.get("draft"))
        self.assertIn("params", fm)
        self.assertEqual(fm["params"].get("status"), "planned")
        self.assertEqual(fm["params"].get("tools"), [])

        body = parts[2]
        self.assertIn("## Purpose", body)
        self.assertIn("## Current status", body)
        self.assertIn("## What I have learned", body)
        self.assertIn("## Next step", body)
        self.assertIn("[Back to Projects](../)", body)

    def test_learning_notebook_structure(self):
        """content/projects/learning-notebook/index.md has updated front matter and Next step."""
        nb_path = os.path.join(self.repo_root, "content", "projects", "learning-notebook", "index.md")
        self.assertTrue(os.path.exists(nb_path), "learning-notebook/index.md not found")

        with open(nb_path, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        self.assertEqual(fm.get("draft"), False)
        self.assertIn("description", fm)
        self.assertEqual(fm.get("params", {}).get("status"), "in-progress")
        self.assertEqual(fm.get("params", {}).get("tools"), ["Hugo", "Markdown"])

        body = parts[2]
        self.assertIn("## Current status", body)
        self.assertIn("making its project descriptions more consistent", body)
        self.assertIn("## Next step", body)
        self.assertIn("Use the same small set of fields and headings", body)

    def test_reading_list_structure(self):
        """content/projects/reading-list/index.md has valid metadata and complete truthful body."""
        rl_path = os.path.join(self.repo_root, "content", "projects", "reading-list", "index.md")
        self.assertTrue(os.path.exists(rl_path), "reading-list/index.md not found")

        with open(rl_path, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        self.assertEqual(fm.get("title"), "My website reading list")
        self.assertEqual(fm.get("draft"), False)
        self.assertEqual(fm.get("params", {}).get("status"), "planned")
        self.assertEqual(fm.get("params", {}).get("tools"), ["Markdown"])

        body = parts[2]
        self.assertIn("## Purpose", body)
        self.assertIn("## Current status", body)
        self.assertIn("## What I have learned", body)
        self.assertIn("## Next step", body)
        self.assertIn("[Back to Projects](../)", body)

    def test_projects_section_index_links(self):
        """content/projects/_index.md links to both learning-notebook and reading-list."""
        idx_path = os.path.join(self.repo_root, "content", "projects", "_index.md")
        self.assertTrue(os.path.exists(idx_path), "content/projects/_index.md not found")

        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[My knowledge notebook](learning-notebook/)", content)
        self.assertIn("[My website reading list](reading-list/)", content)

    def test_reading_list_links_resolve(self):
        """Links in reading-list/index.md must resolve to valid target files in content/."""
        rl_dir = os.path.join(self.repo_root, "content", "projects", "reading-list")
        
        # Test ../ (points to content/projects/_index.md)
        projects_target = os.path.normpath(os.path.join(rl_dir, "..", "_index.md"))
        self.assertTrue(os.path.exists(projects_target), f"Back to projects destination missing: {projects_target}")

        # Test ../../resources/ (points to content/resources/index.md or _index.md)
        resources_target = os.path.normpath(os.path.join(rl_dir, "..", "..", "resources", "index.md"))
        self.assertTrue(os.path.exists(resources_target), f"Resources page destination missing: {resources_target}")

if __name__ == "__main__":
    unittest.main()
