import os
import subprocess
import unittest

class TestChapter11(unittest.TestCase):
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

    def test_template_architecture_files_exist(self):
        """All 6 refactored template files should exist in their designated locations."""
        expected_files = [
            os.path.join(self.repo_root, "layouts", "baseof.html"),
            os.path.join(self.repo_root, "layouts", "all.html"),
            os.path.join(self.repo_root, "layouts", "projects", "section.html"),
            os.path.join(self.repo_root, "layouts", "_partials", "footer.html"),
            os.path.join(self.repo_root, "layouts", "_partials", "page-meta.html"),
            os.path.join(self.repo_root, "layouts", "_partials", "project-list.html"),
        ]
        for fpath in expected_files:
            self.assertTrue(os.path.exists(fpath), f"Expected template file missing: {fpath}")

    def test_baseof_and_define_contract(self):
        """baseof.html should declare block 'main', and content templates must define it."""
        baseof_path = os.path.join(self.repo_root, "layouts", "baseof.html")
        with open(baseof_path, "r", encoding="utf-8") as f:
            baseof_content = f.read()
        self.assertIn('{{ block "main" . }}{{ end }}', baseof_content)
        self.assertIn('{{ partial "footer.html" . }}', baseof_content)

        all_path = os.path.join(self.repo_root, "layouts", "all.html")
        with open(all_path, "r", encoding="utf-8") as f:
            all_content = f.read()
        self.assertIn('{{ define "main" }}', all_content)
        self.assertIn('{{ partial "page-meta.html" . }}', all_content)

        section_path = os.path.join(self.repo_root, "layouts", "projects", "section.html")
        with open(section_path, "r", encoding="utf-8") as f:
            section_content = f.read()
        self.assertIn('{{ define "main" }}', section_content)
        self.assertIn('{{ partial "project-list.html" . }}', section_content)

    def test_projects_landing_page_intro_sentence(self):
        """Projects landing page has the layout-specific sentence, but other pages do not."""
        proj_html = os.path.join(self.public_dir, "projects", "index.html")
        with open(proj_html, "r", encoding="utf-8") as f:
            content = f.read()
        target_sentence = "Choose a project to see its purpose, progress, and next step."
        self.assertIn(target_sentence, content)

        # Confirm sentence is NOT present on detail or about pages
        nb_html = os.path.join(self.public_dir, "projects", "learning-notebook", "index.html")
        with open(nb_html, "r", encoding="utf-8") as f:
            self.assertNotIn(target_sentence, f.read())

        about_html = os.path.join(self.public_dir, "about", "index.html")
        with open(about_html, "r", encoding="utf-8") as f:
            self.assertNotIn(target_sentence, f.read())

    def test_rendered_pages_structural_integrity(self):
        """Pages should retain proper document structure, skip-link target, and single footer."""
        for path_parts in [["index.html"], ["about", "index.html"], ["projects", "index.html"]]:
            page_path = os.path.join(self.public_dir, *path_parts)
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read()
            self.assertTrue(html.startswith("<!doctype html>"))
            self.assertIn('id=main', html)
            self.assertEqual(html.count("<footer"), 1, f"Expected exactly 1 footer tag in {page_path}")

    def test_agents_md_updated_file_map(self):
        """AGENTS.md file map should accurately reflect the refactored layout structure."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        with open(agents_path, "r", encoding="utf-8") as f:
            agents_content = f.read()

        self.assertIn("layouts/baseof.html", agents_content)
        self.assertIn("layouts/all.html", agents_content)
        self.assertIn("layouts/projects/section.html", agents_content)
        self.assertIn("layouts/_partials/", agents_content)

if __name__ == "__main__":
    unittest.main()
