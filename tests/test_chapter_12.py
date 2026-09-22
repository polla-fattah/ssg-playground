import json
import os
import subprocess
import unittest

class TestChapter12(unittest.TestCase):
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

    def test_resource_links_json_model(self):
        """assets/data/resource_links.json must adhere to the 5-field record schema and order."""
        data_path = os.path.join(self.repo_root, "assets", "data", "resource_links.json")
        self.assertTrue(os.path.exists(data_path), f"Missing data file: {data_path}")

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3, "Expected exactly 3 resource records")

        expected_titles = [
            "Hugo documentation",
            "Hugo template introduction",
            "Hugo page bundles"
        ]
        actual_titles = [r.get("title") for r in data]
        self.assertEqual(actual_titles, expected_titles, "Records are not in the agreed order")

        for item in data:
            self.assertIn("title", item)
            self.assertIn("url", item)
            self.assertIn("description", item)
            self.assertIn("topics", item)
            self.assertIn("start_here", item)

            self.assertIsInstance(item["title"], str)
            self.assertTrue(item["url"].startswith("https://"))
            self.assertIsInstance(item["description"], str)
            self.assertIsInstance(item["topics"], list)
            self.assertIsInstance(item["start_here"], bool)

        self.assertTrue(data[0]["start_here"])
        self.assertFalse(data[1]["start_here"])
        self.assertFalse(data[2]["start_here"])

    def test_templates_exist(self):
        """Resource directory partial and page layout must exist."""
        partial_path = os.path.join(self.repo_root, "layouts", "_partials", "resource-directory.html")
        page_layout_path = os.path.join(self.repo_root, "layouts", "resources", "page.html")
        self.assertTrue(os.path.exists(partial_path))
        self.assertTrue(os.path.exists(page_layout_path))

    def test_rendered_resources_page_content(self):
        """public/resources/index.html should display directory records while preserving prose."""
        res_html = os.path.join(self.public_dir, "resources", "index.html")
        self.assertTrue(os.path.exists(res_html))

        with open(res_html, "r", encoding="utf-8") as f:
            content = f.read()

        # Check section heading and id
        self.assertIn('website-publishing', content)

        # Check all 3 links
        self.assertIn("https://gohugo.io/documentation/", content)
        self.assertIn("https://gohugo.io/templates/introduction/", content)
        self.assertIn("https://gohugo.io/content-management/page-bundles/", content)

        # Check Start here tag only on the first
        self.assertEqual(content.count("Start here"), 1)
        self.assertIn("Hugo, Reference", content)
        self.assertIn("Hugo, Templates", content)
        self.assertIn("Hugo, Content organisation", content)

        # Retained prose sections from previous chapters
        self.assertIn("How to use these resources", content)
        self.assertIn("Examples from this notebook", content)

    def test_agents_md_updated_with_json_spec(self):
        """AGENTS.md should list data file paths and include resource record type agreements."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        with open(agents_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("assets/data/resource_links.json", text)
        self.assertIn("layouts/resources/page.html", text)
        self.assertIn("layouts/_partials/resource-directory.html", text)
        self.assertIn("start_here (a Boolean)", text)

if __name__ == "__main__":
    unittest.main()
