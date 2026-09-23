import json
import os
import re
import subprocess
import unittest

class TestChapter14(unittest.TestCase):
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

    def test_02_checks_workflow_structure_and_permissions(self):
        """Verifies .github/workflows/checks.yaml exists with trigger, narrow permissions, and steps."""
        wf_path = os.path.join(self.repo_root, ".github", "workflows", "checks.yaml")
        self.assertTrue(os.path.exists(wf_path), f"Missing checks workflow: {wf_path}")

        with open(wf_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Name and trigger
        self.assertIn("name: Check proposed changes", content)
        self.assertIn("pull_request:", content)
        self.assertIn("branches: [main]", content)

        # Narrow permissions: contents: read only (no pages: write or id-token: write)
        self.assertIn("permissions:", content)
        self.assertIn("contents: read", content)
        self.assertNotIn("pages: write", content)
        self.assertNotIn("id-token: write", content)

        # Runner and steps
        self.assertIn("runs-on: ubuntu-24.04", content)
        self.assertIn("hugo --minify --panicOnWarning", content)
        self.assertIn('grep -n \'"start_here": *"\' assets/data/resource_links.json', content)
        self.assertIn("grep -rn '](/' content/", content)
        self.assertIn("content/articles/*/index.md content/projects/*/index.md", content)

    def test_03_rule_1_directory_flags_are_booleans(self):
        """Rule 1: start_here in resource_links.json must be unquoted Booleans."""
        data_path = os.path.join(self.repo_root, "assets", "data", "resource_links.json")
        self.assertTrue(os.path.exists(data_path))

        with open(data_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            data = json.loads(raw_text)

        # Check raw text with the exact grep regex from CI workflow
        quoted_boolean_pattern = re.compile(r'"start_here":\s*"')
        matches = quoted_boolean_pattern.findall(raw_text)
        self.assertEqual(len(matches), 0, "Found quoted start_here flag in resource_links.json!")

        # Check parsed JSON types
        self.assertEqual(len(data), 5, "Expected exactly 5 resource records")
        for item in data:
            self.assertIsInstance(item.get("start_here"), bool, f"start_here is not bool in: {item}")

        # Fifth record check
        actions_record = data[4]
        self.assertEqual(actions_record.get("title"), "GitHub: Actions documentation")
        self.assertEqual(actions_record.get("url"), "https://docs.github.com/en/actions")
        self.assertEqual(actions_record.get("topics"), ["GitHub Actions", "Automation"])
        self.assertIs(actions_record.get("start_here"), False)

    def test_04_rule_2_internal_links_stay_relative(self):
        """Rule 2: Markdown files in content/ must not contain root-relative links '](/'."""
        content_dir = os.path.join(self.repo_root, "content")
        root_relative_pattern = re.compile(r'\]\(/(?!\s)')

        failing_files = []
        for root, _, files in os.walk(content_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        if root_relative_pattern.search(text):
                            failing_files.append(file_path)

        self.assertEqual(
            len(failing_files), 0,
            f"Found root-relative links '](/' in: {failing_files}"
        )

    def test_05_rule_3_articles_and_projects_have_description(self):
        """Rule 3: All article and project index.md bundles must have description in front matter."""
        pages_to_check = [
            os.path.join(self.repo_root, "content", "articles", "first-learning-note", "index.md"),
            os.path.join(self.repo_root, "content", "articles", "publishing-with-github-pages", "index.md"),
            os.path.join(self.repo_root, "content", "projects", "learning-notebook", "index.md"),
            os.path.join(self.repo_root, "content", "projects", "reading-list", "index.md"),
        ]

        desc_pattern = re.compile(r'^description:\s*.+', re.MULTILINE)
        for page_path in pages_to_check:
            self.assertTrue(os.path.exists(page_path), f"Missing page bundle: {page_path}")
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(
                desc_pattern.search(content),
                f"Page bundle missing description front matter: {page_path}"
            )

        # Specifically check first-learning-note
        with open(pages_to_check[0], "r", encoding="utf-8") as f:
            fln_content = f.read()
        self.assertIn(
            'description: "Editing a page in my notebook, checking the result, and recording what changed."',
            fln_content
        )

    def test_06_rendered_html_includes_fifth_resource(self):
        """public/resources/index.html must display the 5th resource link."""
        res_html = os.path.join(self.public_dir, "resources", "index.html")
        self.assertTrue(os.path.exists(res_html))

        with open(res_html, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("GitHub: Actions documentation", html)
        self.assertIn("https://docs.github.com/en/actions", html)
        self.assertIn("The official reference for automating builds, checks, and deployments on GitHub.", html)

if __name__ == "__main__":
    unittest.main()
