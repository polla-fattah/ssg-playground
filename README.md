# SSG Playground - Chapter 11: Build Reusable Hugo Layouts

Welcome to the hands-on playground repository for **Chapter 11** of *Static Site Generators in the Age of AI*.

This branch (`chapter-11`) is **additive from `chapter-10`**. It refactors our single, all-in-one layout (`layouts/all.html`) into a clean, modular architecture: a shared document base template (`layouts/baseof.html`), reusable partials (`layouts/_partials/`), and a dedicated section layout (`layouts/projects/section.html`), while preserving all existing content, styling, links, and behavior.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 11 Goals

- **Modular Template Architecture**: Break down a multi-purpose layout into single-responsibility components without altering the rendered output.
- **Base Template & Blocks**: Establish `layouts/baseof.html` with `{{ block "main" . }}{{ end }}` to define the shared HTML document frame (head, skip-link, header, navigation, main wrapper, and footer).
- **Matching Content Definitions**: Use `{{ define "main" }} ... {{ end }}` in content templates (`all.html` and `section.html`) to inject page-specific markup into the base frame.
- **Component Partials (`_partials/`)**: Extract reusable markup into `layouts/_partials/`:
  - `footer.html`: Global site footer with relative link.
  - `page-meta.html`: Conditional description, status, and tools metadata.
  - `project-list.html`: Sorted list of project pages with titles, descriptions, and statuses.
- **Section-Specific Layout**: Give the Projects section its own template (`layouts/projects/section.html`) that calls `project-list.html` directly, removing section conditionals from general layouts.
- **Scope-Specific Content**: Add a brief introductory sentence only to the Projects landing page.
- **Maintain Accurate Agent Guidance**: Update `AGENTS.md` to reflect the new template file map.
- **Diagnose Block/Define Mismatches**: Catch and fix silent template rendering failures where `hugo build` succeeds but content fails to display.

---

## 📁 What Changed in Chapter 11 (Additive from Chapter 10)

```text
my-knowledge-site/
+-- layouts/
|   +-- baseof.html                            # [NEW] Document frame (head, nav, main block, footer partial)
|   +-- all.html                               # [UPDATED] General fallback layout: define "main" + page-meta partial
|   +-- projects/
|   |   +-- section.html                       # [NEW] Projects landing page layout with intro sentence & project list
|   +-- _partials/
|       +-- footer.html                        # [NEW] Extracted footer component
|       +-- page-meta.html                     # [NEW] Extracted description, status, and tools metadata
|       +-- project-list.html                  # [NEW] Extracted dynamic project list
+-- AGENTS.md                                  # [UPDATED] File map updated to reflect 4-layer layout structure
+-- content/                                   # [Unchanged] Content and Markdown files
+-- static/                                    # [Unchanged] Hand-crafted CSS
+-- hugo.toml                                  # [Unchanged] Site configuration
+-- tests/
    +-- test_chapter_01.py ... test_chapter_10.py
    +-- test_chapter_11.py                     # [NEW] Automated tests for baseof, partials, and section layout
```

---

## 🏛️ Template Responsibilities & Hierarchy

| Template Path | Responsibility | Context (`.`) Passed |
|---|---|---|
| `layouts/baseof.html` | Full HTML document, `<head>`, navigation, `<main>` wrapper, footer call | Current Page |
| `layouts/all.html` | General content fallback (`{{ define "main" }}`) | Current Page |
| `layouts/projects/section.html` | Projects section landing page with introductory sentence | Section Page |
| `layouts/_partials/footer.html` | Site footer markup | Current Page |
| `layouts/_partials/page-meta.html` | Optional description, status, and tools list | Current Page |
| `layouts/_partials/project-list.html` | Sorted list of `.RegularPages` with descriptions and statuses | Section Page |

---

## 🧩 Key Code Implementations

### 1. `layouts/baseof.html`
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ .Title }} | {{ .Site.Title }}</title>
  <link rel="stylesheet" href="{{ "css/site.css" | relURL }}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>
    <p class="site-name">{{ .Site.Title }}</p>
    <nav aria-label="Main navigation">
      <a href="{{ "" | relURL }}">Home</a>
      <a href="{{ "about/" | relURL }}">About</a>
      <a href="{{ "articles/" | relURL }}">Articles</a>
      <a href="{{ "projects/" | relURL }}">Projects</a>
      <a href="{{ "resources/" | relURL }}">Resources</a>
    </nav>
  </header>
  <main id="main" tabindex="-1">
    {{ block "main" . }}{{ end }}
  </main>
  {{ partial "footer.html" . }}
</body>
</html>
```

### 2. `layouts/projects/section.html`
```html
{{ define "main" }}
  <article>
    <h1>{{ .Title }}</h1>
    {{ partial "page-meta.html" . }}
    {{ .Content }}
    <p>Choose a project to see its purpose, progress, and next step.</p>
    {{ partial "project-list.html" . }}
  </article>
{{ end }}
```

---

## 🧪 Automated Testing

Run the automated test suite across all chapters:

```bash
# Run Chapter 11 specific tests:
python -m unittest tests/test_chapter_11.py

# Run all tests across Chapters 1 through 11:
python -m unittest discover tests
```

### Test Coverage in `test_chapter_11.py`:
1. `test_hugo_build_clean`: Verifies clean Hugo build with zero warnings or errors.
2. `test_template_architecture_files_exist`: Confirms all 6 layout files exist in `layouts/`, `layouts/projects/`, and `layouts/_partials/`.
3. `test_baseof_and_define_contract`: Verifies `block "main"` and `define "main"` contract between base and content templates.
4. `test_projects_landing_page_intro_sentence`: Confirms the introductory sentence appears **only** on the Projects landing page.
5. `test_rendered_pages_structural_integrity`: Ensures proper HTML5 doctype, single footer, and `#main` skip link across all generated pages.
6. `test_agents_md_updated_file_map`: Validates that `AGENTS.md` accurately documents `baseof.html`, `all.html`, `section.html`, and `_partials/`.

---

## 🔗 Git Checkpoint

Commit the completed chapter changes:
```bash
git add layouts/all.html layouts/baseof.html layouts/projects/section.html layouts/_partials/ AGENTS.md tests/ README.md
git commit -m "Organise Hugo layouts into a base, section template, and partials"
```
