# SSG Playground — Chapter 03: Organise a Useful Website

Welcome to the hands-on playground repository for **Chapter 3** of *Static Site Generators in the Age of AI*.

This branch (`chapter-03`) is **additive from `chapter-02`**. It expands your two-page starter into a complete, navigable knowledge notebook with **Information Architecture**, **section landing pages**, and **shared site navigation**.

---

## 🎯 Chapter 3 Goal

Transform your website from isolated pages into a coherent, navigable system:
- Add a standalone **About** page
- Provide structured section landing pages for **Articles** and **Projects**
- Add a project description page and a curated **Resources** page
- Implement site-wide navigation in `layouts/all.html` that works across all pages
- Link to major sections directly from the home page under `## Explore the notebook`
- Understand how folder names dictate URLs, and practice recovering from a broken route

---

## 🗺️ Complete Website Structure Map

| Source File | Published Preview URL | Role & Page Type |
| :--- | :--- | :--- |
| `content/_index.md` | `/` | **Home page** (Branch bundle) |
| `content/about/index.md` | `/about/` | **About page** (Standalone leaf page) |
| `content/articles/_index.md` | `/articles/` | **Articles landing page** (Section branch) |
| `content/articles/first-learning-note/index.md` | `/articles/first-learning-note/` | **Article** (Leaf page bundle with image) |
| `content/projects/_index.md` | `/projects/` | **Projects landing page** (Section branch) |
| `content/projects/learning-notebook/index.md` | `/projects/learning-notebook/` | **Project page** (Leaf page bundle) |
| `content/resources/index.md` | `/resources/` | **Resources page** (Standalone leaf page) |

### `_index.md` vs `index.md` Rule:
- **`_index.md` (with underscore)**: Represents a **branch / section bundle** that groups child pages (Home, Articles section, Projects section).
- **`index.md` (without underscore)**: Represents a **leaf page bundle** (About, single article, single project, Resources).

---

## 🚀 How to Run the Website Locally

Start the standard preview server:

```bash
hugo server
```

Open:
```text
http://localhost:1313/
```

Navigate through the top menu: **Home**, **About**, **Articles**, **Projects**, and **Resources**.

---

## 📁 What Changed in Chapter 3 (Additive from Chapter 2)

```text
my-knowledge-site/
├── hugo.toml                                         # Site settings
├── layouts/
│   └── all.html                                      # [UPDATED] Replaced <nav> with 5 site-wide links
├── static/css/site.css                               # Styling
└── content/
    ├── _index.md                                     # [UPDATED] Added "Explore the notebook" section
    ├── about/
    │   └── index.md                                  # [NEW] About page
    ├── articles/
    │   ├── _index.md                                 # [NEW] Section landing page with manual list
    │   └── first-learning-note/                      # From Chapter 2
    │       ├── index.md
    │       └── notebook-preview.png
    ├── projects/
    │   ├── _index.md                                 # [NEW] Projects landing page with manual list
    │   └── learning-notebook/
    │       └── index.md                              # [NEW] Project description page
    └── resources/
        └── index.md                                  # [NEW] Curated resources list
```

---

## ✍️ Guided Exercises for Chapter 3

### 1. The Power of Shared Layouts
- Notice `layouts/all.html`: By updating only the `<nav>` element, every single page on the site now displays the same navigation row.

### 2. Relative Link Calculations
- From `/about/`: `../articles/first-learning-note/` goes up to root, then down to the article.
- From `/projects/learning-notebook/`: `../../articles/first-learning-note/` goes up 2 levels (`../` to projects, `../../` to root), then down to articles.
- From `/projects/learning-notebook/`: `[Back to Projects](../)` steps up one level.

### 3. Break and Repair a Route
1. Rename folder `content/projects/learning-notebook` to `learning-notebook-test`.
2. Notice that the page now lives at `/projects/learning-notebook-test/`, but the links on `/projects/` still point to `/projects/learning-notebook/` (yielding 404).
3. Hard-refresh your browser (`Ctrl + Shift + R` or `Cmd + Shift + R`) to avoid browser cache.
4. Rename the folder back to `learning-notebook` to restore the working route.

---

## 🧪 Automated Tests

Run the Chapter 3 automated tests:

```bash
python -m unittest tests/test_chapter_03.py
```

Run the full suite across all three chapters (19 assertions):

```bash
python -m unittest discover tests
```

Expected output:
```text
...................
----------------------------------------------------------------------
Ran 19 tests in 0.55s

OK
```

---

## 🛠️ Common Troubleshooting

| Issue | Cause & Fix |
| :--- | :--- |
| **Only navigation appears, rest of page is gone** | You accidentally replaced the entire `layouts/all.html` instead of just replacing the `<nav>...</nav>` block. |
| **Articles page has title but no links** | Make sure you saved the Markdown list body in `content/articles/_index.md`. |
| **Browser shows old page after rename** | Browser cached the response. Use `Ctrl + Shift + R` (hard refresh) or restart Hugo. |
| **Section returns 404** | Verify the section file is named `_index.md` with an underscore, not `index.md`. |

---

## ⏭️ What's Next?
In **Chapter 4**, we will open Developer Tools and inspect the actual **HTML structure** behind these pages, connecting your Markdown source directly to browser elements.
