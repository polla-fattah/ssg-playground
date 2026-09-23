import os
import re
import subprocess
import unittest

class TestChapter15(unittest.TestCase):
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

    def test_02_hugo_toml_site_description(self):
        """hugo.toml must define params.description for site-wide fallback."""
        config_path = os.path.join(self.repo_root, "hugo.toml")
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[params]", content)
        self.assertIn("description =", content)
        self.assertIn("Learning notes, small projects, and useful references", content)

    def test_03_baseof_html_head_and_nav(self):
        """layouts/baseof.html must have conditional title, description fallback, canonical, RSS, and search link."""
        baseof_path = os.path.join(self.repo_root, "layouts", "baseof.html")
        with open(baseof_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Conditional title
        self.assertIn(".IsHome", content)
        self.assertIn(".Site.Title", content)

        # Meta description fallback
        self.assertIn('<meta name="description"', content)
        self.assertIn(".Site.Params.description", content)

        # Canonical link
        self.assertIn('<link rel="canonical" href="{{ .Permalink }}">', content)

        # RSS autodiscovery with $.Site.Title
        self.assertIn('.OutputFormats.Get "rss"', content)
        self.assertIn("$.Site.Title", content)

        # Navigation Search link
        self.assertIn('search/" | relURL', content)

    def test_04_search_content_and_layout(self):
        """content/search/index.md and layouts/search/page.html must exist with required markup."""
        content_path = os.path.join(self.repo_root, "content", "search", "index.md")
        layout_path = os.path.join(self.repo_root, "layouts", "search", "page.html")

        self.assertTrue(os.path.exists(content_path))
        self.assertTrue(os.path.exists(layout_path))

        with open(content_path, "r", encoding="utf-8") as f:
            c_text = f.read()
        self.assertIn('title: "Search"', c_text)
        self.assertIn('draft: false', c_text)

        with open(layout_path, "r", encoding="utf-8") as f:
            l_text = f.read()
        self.assertIn('role="search"', l_text)
        self.assertIn('id="search-query"', l_text)
        self.assertIn('id="search-status"', l_text)
        self.assertIn('id="search-index"', l_text)
        self.assertIn('search-item', l_text)
        self.assertIn('.Site.RegularPages', l_text)
        self.assertIn('ne .RelPermalink $.RelPermalink', l_text)
        self.assertIn('js/search.js', l_text)

    def test_05_search_js_implementation(self):
        """static/js/search.js must implement client-side filtering and guard clauses."""
        js_path = os.path.join(self.repo_root, "static", "js", "search.js")
        self.assertTrue(os.path.exists(js_path))

        with open(js_path, "r", encoding="utf-8") as f:
            js_text = f.read()

        self.assertIn("search-query", js_text)
        self.assertIn("search-index", js_text)
        self.assertIn("search-status", js_text)
        self.assertIn("item.hidden = !match", js_text)
        self.assertIn("preventDefault", js_text)
        self.assertIn('input.addEventListener("input", filter)', js_text)

    def test_06_css_search_styles(self):
        """static/css/site.css must include .search-item[hidden] { display: none; } rule."""
        css_path = os.path.join(self.repo_root, "static", "css", "site.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_text = f.read()

        self.assertIn(".search-item[hidden]", css_text)
        self.assertIn("display: none", css_text)

    def test_07_about_and_resources_have_descriptions(self):
        """content/about/index.md and content/resources/index.md must have front matter descriptions."""
        about_path = os.path.join(self.repo_root, "content", "about", "index.md")
        res_path = os.path.join(self.repo_root, "content", "resources", "index.md")

        with open(about_path, "r", encoding="utf-8") as f:
            about_text = f.read()
        with open(res_path, "r", encoding="utf-8") as f:
            res_text = f.read()

        self.assertIn("description:", about_text)
        self.assertIn("description:", res_text)

    def test_08_agents_md_updated_with_search_files(self):
        """AGENTS.md must list search layout and script paths."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        with open(agents_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("layouts/search/page.html", text)
        self.assertIn("static/js/search.js", text)

    def test_09_rendered_html_verification(self):
        """Verify rendered public files for titles, descriptions, RSS links, and search indexing."""
        # 1. Home page: title should be site title alone, description should be site fallback, has RSS
        home_path = os.path.join(self.public_dir, "index.html")
        with open(home_path, "r", encoding="utf-8") as f:
            home_html = f.read()

        self.assertIn("<title>My Knowledge Notebook</title>", home_html)
        self.assertIn("Learning notes, small projects, and useful references", home_html)
        self.assertIn("application/rss+xml", home_html)
        self.assertIn("canonical", home_html)
        self.assertIn("search/", home_html)

        # 2. Search page: title is 'Search | My Knowledge Notebook', has 6 items, does not list search itself
        search_path = os.path.join(self.public_dir, "search", "index.html")
        self.assertTrue(os.path.exists(search_path))
        with open(search_path, "r", encoding="utf-8") as f:
            search_html = f.read()

        self.assertIn("<title>Search | My Knowledge Notebook</title>", search_html)
        self.assertIn("Find a page in this notebook by its title or description.", search_html)
        self.assertEqual(search_html.count("search-item"), 6)
        self.assertIn("About this notebook", search_html)
        self.assertIn("My first learning note", search_html)
        self.assertIn("What I learned publishing with GitHub Pages", search_html)
        self.assertIn("My knowledge notebook", search_html)
        self.assertIn("My website reading list", search_html)
        self.assertIn("Resources", search_html)
        self.assertNotIn("search/>Search</a><p>", search_html)

        # 3. Article page: does not have RSS feed link in head
        article_path = os.path.join(self.public_dir, "articles", "first-learning-note", "index.html")
        with open(article_path, "r", encoding="utf-8") as f:
            art_html = f.read()
        self.assertNotIn('type="application/rss+xml"', art_html)

        # 4. XML files exist in public/
        sitemap_path = os.path.join(self.public_dir, "sitemap.xml")
        rss_path = os.path.join(self.public_dir, "index.xml")
        self.assertTrue(os.path.exists(sitemap_path))
        self.assertTrue(os.path.exists(rss_path))

if __name__ == "__main__":
    unittest.main()
