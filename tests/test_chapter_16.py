import os
import re
import subprocess
import tomllib
import unittest

class TestChapter16(unittest.TestCase):
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

    def test_02_hugo_toml_multilingual_config(self):
        """hugo.toml must configure en and ckb with defaultContentLanguageInSubdir = false."""
        config_path = os.path.join(self.repo_root, "hugo.toml")
        with open(config_path, "rb") as f:
            cfg = tomllib.load(f)

        self.assertEqual(cfg.get("defaultContentLanguage"), "en")
        self.assertFalse(cfg.get("defaultContentLanguageInSubdir"))
        self.assertIn("languages", cfg)
        langs = cfg["languages"]
        self.assertIn("en", langs)
        self.assertIn("ckb", langs)

        ckb_cfg = langs["ckb"]
        # Check direction is rtl (supports either direction or legacy languageDirection)
        dir_val = ckb_cfg.get("direction") or ckb_cfg.get("languageDirection")
        self.assertEqual(dir_val, "rtl")

    def test_03_baseof_and_partials(self):
        """layouts/baseof.html and partials must use language-aware markup, i18n, and relLangURL."""
        baseof_path = os.path.join(self.repo_root, "layouts", "baseof.html")
        footer_path = os.path.join(self.repo_root, "layouts", "_partials", "footer.html")
        lang_links_path = os.path.join(self.repo_root, "layouts", "_partials", "language-links.html")

        self.assertTrue(os.path.exists(baseof_path))
        self.assertTrue(os.path.exists(footer_path))
        self.assertTrue(os.path.exists(lang_links_path))

        with open(baseof_path, "r", encoding="utf-8") as f:
            baseof_text = f.read()
        with open(footer_path, "r", encoding="utf-8") as f:
            footer_text = f.read()
        with open(lang_links_path, "r", encoding="utf-8") as f:
            lang_links_text = f.read()

        # HTML tag has lang and dir attributes
        self.assertIn("<html", baseof_text)
        self.assertIn("lang=", baseof_text)
        self.assertIn("dir=", baseof_text)

        # Nav uses i18n and relLangURL
        self.assertIn('i18n "nav_home"', baseof_text)
        self.assertIn('i18n "nav_label"', baseof_text)
        self.assertIn('relLangURL', baseof_text)

        # Footer About link uses relLangURL
        self.assertIn('about/" | relLangURL', footer_text)

        # Language links partial uses .Translations
        self.assertIn(".Translations", lang_links_text)
        self.assertIn(".RelPermalink", lang_links_text)

    def test_04_i18n_files_keys_parity(self):
        """i18n/en.toml and i18n/ckb.toml must exist and have matching keys."""
        en_path = os.path.join(self.repo_root, "i18n", "en.toml")
        ckb_path = os.path.join(self.repo_root, "i18n", "ckb.toml")

        self.assertTrue(os.path.exists(en_path))
        self.assertTrue(os.path.exists(ckb_path))

        with open(en_path, "rb") as f:
            en_data = tomllib.load(f)
        with open(ckb_path, "rb") as f:
            ckb_data = tomllib.load(f)

        expected_keys = {
            "nav_home", "nav_about", "nav_articles", "nav_projects",
            "nav_resources", "nav_search", "nav_label", "languages_label"
        }
        self.assertTrue(expected_keys.issubset(set(en_data.keys())))
        self.assertEqual(set(en_data.keys()), set(ckb_data.keys()))

    def test_05_css_logical_properties_and_rtl(self):
        """static/css/site.css must use inset-inline-start on .skip-link and define :lang(ckb)."""
        css_path = os.path.join(self.repo_root, "static", "css", "site.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_text = f.read()

        self.assertIn("inset-inline-start:", css_text)
        self.assertNotIn("left: 1rem;", css_text)
        self.assertIn(".language-links", css_text)
        self.assertIn(":lang(ckb)", css_text)

    def test_06_kurdish_content_source_checked(self):
        """Kurdish content files must exist, have draft: false, and declare source_checked date."""
        ckb_home = os.path.join(self.repo_root, "content", "_index.ckb.md")
        ckb_about = os.path.join(self.repo_root, "content", "about", "index.ckb.md")

        self.assertTrue(os.path.exists(ckb_home))
        self.assertTrue(os.path.exists(ckb_about))

        for file_path in [ckb_home, ckb_about]:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.assertIn("draft: false", text)
            self.assertIn("source_checked:", text)

    def test_07_checks_workflow_includes_translation_rule(self):
        """.github/workflows/checks.yaml must include source_checked validation."""
        wf_path = os.path.join(self.repo_root, ".github", "workflows", "checks.yaml")
        with open(wf_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("Check that translations record a source check", text)
        self.assertIn("source_checked:", text)

    def test_08_agents_md_updated_with_i18n(self):
        """AGENTS.md must document i18n files, ckb pages, language switcher, and translation agreement."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        with open(agents_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.assertIn("i18n/en.toml", text)
        self.assertIn("i18n/ckb.toml", text)
        self.assertIn(".ckb.md", text)
        self.assertIn("layouts/_partials/language-links.html", text)
        self.assertIn("Translations keep English front-matter field names", text)

    def test_09_rendered_multilingual_pages(self):
        """Verify rendered HTML for both English and Kurdish pages."""
        # 1. English home page
        en_home_path = os.path.join(self.public_dir, "index.html")
        with open(en_home_path, "r", encoding="utf-8") as f:
            en_home = f.read()

        self.assertIn("lang=en", en_home)
        self.assertIn("dir=ltr", en_home)
        self.assertIn("language-links", en_home)
        self.assertIn("ckb/", en_home)

        # 2. Kurdish home page
        ckb_home_path = os.path.join(self.public_dir, "ckb", "index.html")
        self.assertTrue(os.path.exists(ckb_home_path))
        with open(ckb_home_path, "r", encoding="utf-8") as f:
            ckb_home = f.read()

        self.assertIn("lang=ckb", ckb_home)
        self.assertIn("dir=rtl", ckb_home)
        self.assertIn("تێبینییەکانی من", ckb_home)
        self.assertIn("language-links", ckb_home)
        self.assertIn("English", ckb_home)

        # Kurdish nav links point to /ckb/...
        self.assertIn("ckb/about/", ckb_home)
        self.assertIn("ckb/articles/", ckb_home)

        # Kurdish footer links to /ckb/about/
        self.assertIn('Read <a href=/my-knowledge-site/ckb/about/>about this notebook</a>', ckb_home)

        # 3. Language switcher on About pages
        en_about_path = os.path.join(self.public_dir, "about", "index.html")
        ckb_about_path = os.path.join(self.public_dir, "ckb", "about", "index.html")

        self.assertTrue(os.path.exists(en_about_path))
        self.assertTrue(os.path.exists(ckb_about_path))

        with open(en_about_path, "r", encoding="utf-8") as f:
            en_about = f.read()
        with open(ckb_about_path, "r", encoding="utf-8") as f:
            ckb_about = f.read()

        self.assertIn("ckb/about/", en_about)
        self.assertIn('href=/my-knowledge-site/about/', ckb_about)

        # 4. Untranslated page (Articles) shows NO language switcher
        articles_path = os.path.join(self.public_dir, "articles", "index.html")
        with open(articles_path, "r", encoding="utf-8") as f:
            art_html = f.read()
        self.assertNotIn("language-links", art_html)

if __name__ == "__main__":
    unittest.main()
