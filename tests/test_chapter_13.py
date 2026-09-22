import json
import os
import re
import subprocess
import unittest

class TestChapter13(unittest.TestCase):
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

    def test_02_sources_publishing_notes_exists_and_not_published(self):
        """sources/publishing-notes.md exists, contains raw notes and gaps, and is not published into public/."""
        notes_path = os.path.join(self.repo_root, "sources", "publishing-notes.md")
        self.assertTrue(os.path.exists(notes_path), f"Missing sources file: {notes_path}")

        with open(notes_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Raw notes: publishing the notebook", content)
        self.assertIn("Not measured: how long a deployment usually takes", content)
        self.assertIn("Not attempted: a custom domain", content)
        self.assertIn("https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", content)

        # Hugo must not publish sources/ into public/
        rendered_sources = os.path.join(self.public_dir, "sources", "index.html")
        self.assertFalse(os.path.exists(rendered_sources), "sources/ folder was unexpectedly published as a web page")

    def test_03_agents_md_updated_with_sourcing_and_attribution(self):
        """AGENTS.md must document sources/, article paths, and content sourcing/attribution agreements."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        self.assertTrue(os.path.exists(agents_path))

        with open(agents_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Path entries under Files
        self.assertIn("sources/", content)
        self.assertIn("content/articles/", content)
        self.assertIn("content/articles/_index.md", content)
        self.assertIn("content/_index.md", content)

        # Working agreements
        self.assertIn("For content tasks, use only the source files named in the task", content)
        self.assertIn("Do not state anything the named source does not support", content)
        self.assertIn("Credit every external reference in a Sources section in the page body", content)
        self.assertIn("Leave new pages at draft: true. Publication is the reader's decision", content)

    def test_04_article_file_structure_and_model(self):
        """content/articles/publishing-with-github-pages/index.md must follow the agreed model and word limit."""
        article_path = os.path.join(
            self.repo_root,
            "content",
            "articles",
            "publishing-with-github-pages",
            "index.md"
        )
        self.assertTrue(os.path.exists(article_path), f"Missing article: {article_path}")

        with open(article_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Front matter checks
        self.assertIn('title: "What I learned publishing with GitHub Pages"', content)
        self.assertIn('draft: false', content)
        self.assertIn('description:', content)

        # Heading order checks
        h1 = content.find("## What this is about")
        h2 = content.find("## What happened")
        h3 = content.find("## What I would do differently")
        h4 = content.find("## Sources")

        self.assertNotEqual(h1, -1, "Missing heading: ## What this is about")
        self.assertNotEqual(h2, -1, "Missing heading: ## What happened")
        self.assertNotEqual(h3, -1, "Missing heading: ## What I would do differently")
        self.assertNotEqual(h4, -1, "Missing heading: ## Sources")
        self.assertTrue(h1 < h2 < h3 < h4, "Headings are not in the agreed order")

        # Unsupported statement test (must NOT be present in published version)
        self.assertNotIn(
            "Deployments usually finish in under a minute",
            content,
            "The unsupported claim experiment was not removed before publication"
        )

        # Sources link check
        self.assertIn("https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", content)

        # Word count check (body under 400 words)
        body = content[h1:]
        words = len(body.split())
        self.assertLessEqual(words, 400, f"Article body exceeds 400 words: {words}")

    def test_05_manual_list_links_in_content(self):
        """content/articles/_index.md and content/_index.md must link to the new article."""
        articles_index = os.path.join(self.repo_root, "content", "articles", "_index.md")
        home_index = os.path.join(self.repo_root, "content", "_index.md")

        with open(articles_index, "r", encoding="utf-8") as f:
            art_text = f.read()
        with open(home_index, "r", encoding="utf-8") as f:
            home_text = f.read()

        # Articles landing page: relative link within articles section
        self.assertIn("publishing-with-github-pages/", art_text)

        # Home page: relative link from site root
        self.assertIn("articles/publishing-with-github-pages/", home_text)

    def test_06_resource_links_json_contains_four_records(self):
        """assets/data/resource_links.json must contain 4 records with the 5 schema fields."""
        data_path = os.path.join(self.repo_root, "assets", "data", "resource_links.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 4, "Expected exactly 4 resource records")
        github_record = data[3]
        self.assertEqual(github_record.get("title"), "GitHub: configuring a publishing source")
        self.assertEqual(
            github_record.get("url"),
            "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site"
        )
        self.assertEqual(github_record.get("topics"), ["GitHub Pages", "Publishing"])
        self.assertIs(github_record.get("start_here"), False)

        # Ensure only 1 record has start_here = true
        start_here_count = sum(1 for r in data if r.get("start_here") is True)
        self.assertEqual(start_here_count, 1, "Only one record should have start_here: true")

    def test_07_rendered_public_pages(self):
        """public/ html files must correctly display article, links, and updated directory."""
        # Article page rendered
        article_html = os.path.join(
            self.public_dir,
            "articles",
            "publishing-with-github-pages",
            "index.html"
        )
        self.assertTrue(os.path.exists(article_html), "Article page not found in public/")
        with open(article_html, "r", encoding="utf-8") as f:
            art_html_content = f.read()
        self.assertIn("What I learned publishing with GitHub Pages", art_html_content)
        self.assertIn("What this is about", art_html_content)
        self.assertIn("What happened", art_html_content)
        self.assertIn("What I would do differently", art_html_content)
        self.assertIn("Sources", art_html_content)

        # Articles landing page rendered
        articles_list_html = os.path.join(self.public_dir, "articles", "index.html")
        with open(articles_list_html, "r", encoding="utf-8") as f:
            art_list_content = f.read()
        self.assertIn("publishing-with-github-pages/", art_list_content)

        # Home page rendered
        home_html = os.path.join(self.public_dir, "index.html")
        with open(home_html, "r", encoding="utf-8") as f:
            home_content = f.read()
        self.assertIn("articles/publishing-with-github-pages/", home_content)

        # Resources directory rendered
        resources_html = os.path.join(self.public_dir, "resources", "index.html")
        with open(resources_html, "r", encoding="utf-8") as f:
            res_content = f.read()
        self.assertIn("GitHub: configuring a publishing source", res_content)
        self.assertIn("https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", res_content)

if __name__ == "__main__":
    unittest.main()
