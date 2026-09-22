# SSG Playground — Chapter 02: Write and Publish Content Locally

Welcome to the hands-on playground repository for **Chapter 2** of *Static Site Generators in the Age of AI*.

This branch (`chapter-02`) is **additive from `chapter-01`**. It introduces your website's **first article**, demonstrates **leaf page bundles**, teaches structured **Markdown**, and connects the new article to the home page.

---

## 🎯 Chapter 2 Goal

Give your website its first readable article with:
- Structured sections, lists, emphasis, and code snippets
- Embedded screenshot image with meaningful alternative text
- Safe internal, external, and in-page anchor links
- Working draft toggling (`draft: true` vs `draft: false`)
- Discoverability via a link on the home page

---

## 🚀 How to Run the Website Locally

### 1. Preview Including Drafts
When drafting a new article (`draft: true` in front matter), start Hugo with the `-D` flag:

```bash
hugo server -D
```

Open:
```text
http://localhost:1313/articles/first-learning-note/
```

### 2. Normal Preview (Published Content Only)
When your article is finished and set to `draft: false`:

```bash
hugo server
```

*(Without `-D`, any file with `draft: true` is excluded from the site).*

---

## 📁 What Changed in Chapter 2 (Additive from Chapter 1)

```text
my-knowledge-site/
├── hugo.toml                                         # Inherited from Chapter 1
├── layouts/all.html                                  # Inherited from Chapter 1
├── static/css/site.css                               # [UPDATED] Added article img & pre rules
└── content/
    ├── _index.md                                     # [UPDATED] Added "Latest writing" section
    └── articles/
        └── first-learning-note/                      # [NEW] Leaf page bundle
            ├── index.md                              # The new article content
            └── notebook-preview.png                  # Embedded screenshot asset
```

### Why `index.md` inside a folder?
Hugo calls a folder containing `index.md` and related media a **leaf page bundle**. This keeps the article text and its images (`notebook-preview.png`) colocated in one self-contained directory.

---

## ✍️ Guided Exercises for Chapter 2

### 1. Front Matter & Draft Control
- Open `content/articles/first-learning-note/index.md`.
- Observe the YAML front matter:
  ```yaml
  ---
  title: "My first learning note"
  draft: false
  ---
  ```
- Change `draft: true`, run `hugo server` (without `-D`), and observe that `/articles/first-learning-note/` returns 404.
- Restart with `hugo server -D` to preview it while drafting.
- Set `draft: false` when ready for normal preview.

### 2. Markdown Formatting Features
- **Headings**: Use `##` for main sections, `###` for subsections.
- **Emphasis**: `**bold**` for important rules, `*italic*` for subtle emphasis.
- **Lists**: Bulleted (`-`) for unordered collections, numbered (`1. 2. 3.`) when order matters.
- **Inline Code & Fences**: Use backticks for commands (`` `content/_index.md` ``) and triple backticks for multiline samples.

### 3. Links and Anchors
- **External link**: `[Hugo documentation](https://gohugo.io/documentation/)`
- **In-page section anchor**: `[Jump to my next step](#my-next-step)` jumps directly to `<h2 id="my-next-step">`.
- **Relative return link**: `[Return to my home page](../../)` navigates up two address levels to the site root.

### 4. Bundled Images & Responsive CSS
- Image syntax: `![Alternative text](notebook-preview.png)`
- Notice that only the filename is needed because the image lives in the same leaf bundle.
- In `static/css/site.css`, the following rules ensure images shrink on mobile screens and code blocks scroll horizontally:
  ```css
  article img { display: block; max-width: 100%; height: auto; }
  article pre { max-width: 100%; overflow-x: auto; }
  ```

### 5. Break Something on Purpose (Missing Image)
- Change `notebook-preview.png` to `notebook-preview-missing.png` in Markdown.
- Notice that Hugo builds without error, but the image fails to load in the browser.
- Restore the correct filename to verify recovery.

---

## 🧪 Automated Tests

Run the Chapter 2 test suite to verify page bundle generation, HTML elements, anchor links, bundled image assets, and CSS:

```bash
python -m unittest tests/test_chapter_02.py
```

To run all tests across Chapter 1 and Chapter 2:
```bash
python -m unittest discover tests
```

Expected output:
```text
.............
----------------------------------------------------------------------
Ran 13 tests in 0.35s

OK
```

---

## 🛠️ Common Troubleshooting

| Problem | Cause & Fix |
| :--- | :--- |
| **Article returns 404** | Check that `draft: false` is set, or that you started Hugo with `hugo server -D`. |
| **Image does not display** | Ensure `notebook-preview.png` is inside `content/articles/first-learning-note/` right next to `index.md`. |
| **Image overflows screen** | Verify that `article img { max-width: 100%; }` is saved at the bottom of `static/css/site.css`. |
| **Return home link goes to wrong page** | From `/articles/first-learning-note/`, you need `../../` (two parent hops) to reach the root. |

---

## ⏭️ What's Next?
In **Chapter 3**, we will organise this into a structured website with an **About** page, sections, categories, and site-wide navigation.
