import os
import subprocess
import unittest

class TestChapter10(unittest.TestCase):
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

    def test_layouts_all_structure(self):
        """Layout templates should contain the required conditional blocks and dynamic section list."""
        all_path = os.path.join(self.repo_root, "layouts", "all.html")
        meta_partial = os.path.join(self.repo_root, "layouts", "_partials", "page-meta.html")
        list_partial = os.path.join(self.repo_root, "layouts", "_partials", "project-list.html")
        
        content = ""
        with open(all_path, "r", encoding="utf-8") as f:
            content += f.read()
        if os.path.exists(meta_partial):
            with open(meta_partial, "r", encoding="utf-8") as f:
                content += f.read()
        if os.path.exists(list_partial):
            with open(list_partial, "r", encoding="utf-8") as f:
                content += f.read()

        # Check metadata conditionals
        self.assertIn("with .Description", content)
        self.assertIn("with .Params.status", content)
        self.assertIn("with .Params.tools", content)
        self.assertIn("range .", content)

        # Check section condition and sorting
        self.assertIn('.RegularPages.ByTitle', content)
        self.assertIn('.RelPermalink', content)

    def test_projects_index_markdown_cleaned(self):
        """content/projects/_index.md should no longer have the manual project list."""
        idx_path = os.path.join(self.repo_root, "content", "projects", "_index.md")
        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertNotIn("## Current work", content)
        self.assertNotIn("learning-notebook/", content)
        self.assertNotIn("reading-list/", content)

    def test_rendered_project_pages_contain_metadata(self):
        """Rendered project HTML pages should display their description, status, and tools."""
        # 1. Learning notebook
        nb_html = os.path.join(self.public_dir, "projects", "learning-notebook", "index.html")
        self.assertTrue(os.path.exists(nb_html))
        with open(nb_html, "r", encoding="utf-8") as f:
            nb_content = f.read()

        self.assertIn("A personal website for learning notes", nb_content)
        self.assertIn("<strong>Status:</strong> in-progress", nb_content)
        self.assertIn("<strong>Tools:</strong>", nb_content)
        self.assertIn("<li>Hugo</li>", nb_content)
        self.assertIn("<li>Markdown</li>", nb_content)

        # 2. Reading list
        rl_html = os.path.join(self.public_dir, "projects", "reading-list", "index.html")
        self.assertTrue(os.path.exists(rl_html))
        with open(rl_html, "r", encoding="utf-8") as f:
            rl_content = f.read()

        self.assertIn("A planned collection of resources", rl_content)
        self.assertIn("<strong>Status:</strong> planned", rl_content)
        self.assertIn("<strong>Tools:</strong>", rl_content)
        self.assertIn("<li>Markdown</li>", rl_content)

    def test_rendered_projects_section_list(self):
        """public/projects/index.html should automatically list all regular project pages with status."""
        proj_html = os.path.join(self.public_dir, "projects", "index.html")
        self.assertTrue(os.path.exists(proj_html))
        with open(proj_html, "r", encoding="utf-8") as f:
            proj_content = f.read()

        self.assertIn("<h2>Current work</h2>", proj_content)
        self.assertIn("/my-knowledge-site/projects/learning-notebook/", proj_content)
        self.assertIn("My knowledge notebook", proj_content)
        self.assertIn("<strong>Status:</strong> in-progress", proj_content)

        self.assertIn("/my-knowledge-site/projects/reading-list/", proj_content)
        self.assertIn("My website reading list", proj_content)
        self.assertIn("<strong>Status:</strong> planned", proj_content)

    def test_non_project_pages_omit_project_metadata(self):
        """Pages without project metadata (e.g. About) should not render empty labels or project lists."""
        about_html = os.path.join(self.public_dir, "about", "index.html")
        self.assertTrue(os.path.exists(about_html))
        with open(about_html, "r", encoding="utf-8") as f:
            about_content = f.read()

        self.assertNotIn("<strong>Status:</strong>", about_content)
        self.assertNotIn("<strong>Tools:</strong>", about_content)
        self.assertNotIn("<h2>Current work</h2>", about_content)

if __name__ == "__main__":
    unittest.main()
