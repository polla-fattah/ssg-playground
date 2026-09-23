import os
import re
import subprocess
import unittest

class TestChapter17(unittest.TestCase):
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

    def test_02_contact_content_file(self):
        """content/contact/index.md must exist with required front matter and plain text email."""
        contact_md = os.path.join(self.repo_root, "content", "contact", "index.md")
        self.assertTrue(os.path.exists(contact_md), "content/contact/index.md missing")

        with open(contact_md, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('title: "Contact"', content)
        self.assertIn('description:', content)
        self.assertIn('contact_address:', content)
        self.assertIn('you@example.org', content)
        # Check plain text email alternative exists
        self.assertTrue(
            '`you@example.org`' in content or 'you@example.org' in content,
            "Plain text fallback email address missing in content/contact/index.md"
        )

    def test_03_contact_layout_template(self):
        """layouts/contact/page.html must exist with accessible form markup and defer script."""
        layout_path = os.path.join(self.repo_root, "layouts", "contact", "page.html")
        self.assertTrue(os.path.exists(layout_path), "layouts/contact/page.html missing")

        with open(layout_path, "r", encoding="utf-8") as f:
            tmpl = f.read()

        # Check form element and attributes
        self.assertIn('<form class="contact-form" id="contact-form" novalidate', tmpl)
        self.assertIn('data-address="{{ .Params.contact_address }}"', tmpl)

        # Check controls have matching labels
        self.assertIn('<label for="contact-name">', tmpl)
        self.assertIn('id="contact-name"', tmpl)
        self.assertIn('name="name"', tmpl)
        self.assertIn('autocomplete="name"', tmpl)

        self.assertIn('<label for="contact-subject">', tmpl)
        self.assertIn('id="contact-subject"', tmpl)
        self.assertIn('name="subject"', tmpl)

        self.assertIn('<label for="contact-message">', tmpl)
        self.assertIn('id="contact-message"', tmpl)
        self.assertIn('name="message"', tmpl)

        # Check submit button and status container
        self.assertIn('<button type="submit">', tmpl)
        self.assertIn('id="contact-status"', tmpl)
        self.assertIn('role="status"', tmpl)

        # Script inclusion
        self.assertIn('js/contact.js', tmpl)
        self.assertIn('defer', tmpl)

    def test_04_contact_script(self):
        """static/js/contact.js must handle submission, validate fields, and build encoded mailto href."""
        js_path = os.path.join(self.repo_root, "static", "js", "contact.js")
        self.assertTrue(os.path.exists(js_path), "static/js/contact.js missing")

        with open(js_path, "r", encoding="utf-8") as f:
            js = f.read()

        # Key mechanics in script
        self.assertIn("contact-form", js)
        self.assertIn("contact-status", js)
        self.assertIn("event.preventDefault()", js)
        self.assertIn(".trim()", js)
        self.assertIn("encodeURIComponent(subject)", js)
        self.assertIn("encodeURIComponent(body)", js)
        self.assertIn("mailto:", js)
        self.assertIn("window.location.href", js)

    def test_05_css_contact_styling(self):
        """static/css/site.css must style contact form and inherit font family."""
        css_path = os.path.join(self.repo_root, "static", "css", "site.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        self.assertIn(".contact-form label", css)
        self.assertIn(".contact-form input", css)
        self.assertIn("font-family: inherit;", css)
        self.assertIn(".contact-error", css)

    def test_06_footer_and_navigation(self):
        """layouts/_partials/footer.html must link to contact page."""
        footer_path = os.path.join(self.repo_root, "layouts", "_partials", "footer.html")
        with open(footer_path, "r", encoding="utf-8") as f:
            footer = f.read()

        self.assertIn('contact/" | relLangURL', footer)

    def test_07_agents_guidance_updated(self):
        """AGENTS.md must list contact files and record working agreement."""
        agents_path = os.path.join(self.repo_root, "AGENTS.md")
        with open(agents_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("layouts/contact/page.html", content)
        self.assertIn("static/js/contact.js", content)
        self.assertIn("The contact form prepares a message in the visitor's own mail client", content)
        self.assertIn("sends nothing to any server", content)

    def test_08_rendered_html_output(self):
        """public/contact/index.html must render with full semantic markup and data-address."""
        contact_html = os.path.join(self.public_dir, "contact", "index.html")
        self.assertTrue(os.path.exists(contact_html), "public/contact/index.html not generated")

        with open(contact_html, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("<form", html)
        self.assertTrue('id="contact-form"' in html or 'id=contact-form' in html)
        self.assertTrue('data-address="you@example.org"' in html or 'data-address=you@example.org' in html)
        self.assertTrue('role="status"' in html or 'role=status' in html)
        self.assertIn("/js/contact.js", html)
        self.assertIn("send a message", html)

if __name__ == "__main__":
    unittest.main()
