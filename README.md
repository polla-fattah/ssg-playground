# SSG Playground - Chapter 09: Give Your Hugo Content a Consistent Structure

Welcome to the hands-on playground repository for **Chapter 9** of *Static Site Generators in the Age of AI*.

This branch (`chapter-09`) is **additive from `chapter-08`**. It establishes a clear, predictable **content model** across project pages, introduces Hugo **archetypes** as reusable starters, covers clean YAML front matter editing, and adds a second project page for a planned reading list.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

##  Chapter 9 Goals

- **Define a Content Model**: Agree on a minimal, purposeful schema for project pages without overcomplicating fields.
- **Master Practical YAML**: Safely write and edit strings, booleans, nested mappings, and lists in Hugo front matter.
- **Separate Readiness from Progress**: Distinguish page publication state (`draft: false`) from real-world project status (`params.status: "planned"`).
- **Create an Archetype Starter**: Write `archetypes/projects.md` and generate new content using `hugo new content --kind projects projects/reading-list/index.md`.
- **Maintain Section Navigation**: Add the new project to the manual section index in `content/projects/_index.md`.
- **Catch & Fix Syntax Errors**: Deliberately test malformed YAML with `hugo --minify --panicOnWarning` and repair it.

---

##  What Changed in Chapter 9 (Additive from Chapter 8)

```text
my-knowledge-site/
+-- archetypes/
|   +-- projects.md                            # [NEW] Reusable starter template for project pages
+-- content/
|   +-- projects/
|       +-- _index.md                          # [UPDATED] Added link to the new reading-list project
|       +-- learning-notebook/
|       |   +-- index.md                       # [UPDATED] Added description, params.status, params.tools, Next step
|       +-- reading-list/
|           +-- index.md                       # [NEW] Created via archetype; truthful planned reading list
+-- AGENTS.md                                  # [From Chapter 8] Project rules and boundaries
+-- layouts/
|   +-- all.html                               # [From Chapter 4] Minimal base layout (shows title + body)
+-- static/
|   +-- css/site.css                           # [From Chapter 5] Hand-crafted CSS
+-- hugo.toml                                  # [From Chapter 1] Base site configuration
+-- tests/
    +-- test_chapter_01.py ... test_chapter_08.py
    +-- test_chapter_09.py                     # [NEW] Automated tests for content model, archetype, and links
```

---

##  The Project Content Model

A content model is an editorial agreement about the information a specific kind of page should contain:

| Location | Field / Heading | Value Shape | Our Editorial Agreement |
|---|---|---|---|
| **Front Matter** | `title` | Text (quoted string) | A concise, readable project name |
| **Front Matter** | `description` | Text (quoted string) | One sentence explaining the project's purpose |
| **Front Matter** | `draft` | Boolean (`true` / `false`) | Is this page ready for public site builds? |
| **Front Matter** | `params.status` | Choice string | One of: `"planned"`, `"in-progress"`, `"complete"` |
| **Front Matter** | `params.tools` | List of strings | Array of relevant tools (e.g. `["Hugo", "Markdown"]` or `[]`) |
| **Body (Markdown)** | `## Purpose` | Section heading | What the project aims to accomplish |
| **Body (Markdown)** | `## Current status` | Section heading | Truthful explanation of what has actually occurred |
| **Body (Markdown)** | `## What I have learned` | Section heading | Concrete learnings or an honest statement that work has not begun |
| **Body (Markdown)** | `## Next step` | Section heading | One actionable next step or a completion notice |
| **Body (Markdown)** | `[Back to Projects](../)` | Relative link | Navigation back to the parent section |

> **Important Note:** In this chapter, `params.status` and `params.tools` are stored in front matter, but they are **not yet visible** in the browser. Our existing layout (`layouts/all.html`) only outputs `{{ .Title }}` and `{{ .Content }}`. Storing metadata today prepares the site for Chapter 10, where Hugo template expressions, conditions, and loops will display them.

---

##  Key Workflows & Commands

### 1. Creating Content from an Archetype
```bash
# Uses archetypes/projects.md to scaffold the leaf bundle
hugo new content --kind projects projects/reading-list/index.md
```

### 2. Previewing Drafts vs Normal Site
```bash
# Preview drafts while writing and revising:
hugo server -D

# Normal preview (only pages where draft: false appear):
hugo server
```

### 3. Syntax Verification & Panic on Warning
```bash
# Verifies that YAML front matter parses without errors:
hugo --minify --panicOnWarning
```

---

##  Automated Testing

Run the automated test suite across all chapters:

```bash
# Run Chapter 9 specific tests:
python -m unittest tests/test_chapter_09.py

# Run all tests across Chapters 1 through 9:
python -m unittest discover tests
```

### Test Coverage in `test_chapter_09.py`:
1. `test_hugo_build_clean`: Verifies zero warnings and exit code 0 on `--minify --panicOnWarning`.
2. `test_archetype_exists_and_valid`: Verifies `archetypes/projects.md` exists with all required front matter keys and body section prompts.
3. `test_learning_notebook_structure`: Verifies `content/projects/learning-notebook/index.md` has `status: "in-progress"`, tools `["Hugo", "Markdown"]`, and the new `Next step` section.
4. `test_reading_list_structure`: Verifies `content/projects/reading-list/index.md` has `status: "planned"`, tool `["Markdown"]`, `draft: false`, and all 4 body sections.
5. `test_projects_section_index_links`: Verifies `content/projects/_index.md` links to both projects.
6. `test_reading_list_links_resolve`: Verifies that `../../resources/` and `../` resolve to physical files on disk.

---

##  Git Checkpoint

Commit the four chapter files cleanly:
```bash
git add archetypes/projects.md content/projects/_index.md content/projects/learning-notebook/index.md content/projects/reading-list/index.md tests/test_chapter_09.py README.md
git commit -m "Define a consistent project model and add a reading-list project"
```
