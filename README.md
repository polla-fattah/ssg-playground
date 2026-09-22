# SSG Playground — Chapter 04: Understand the HTML Behind Your Pages

Welcome to the hands-on playground repository for **Chapter 4** of *Static Site Generators in the Age of AI*.

This branch (`chapter-04`) is **additive from `chapter-03`**. It focuses on demystifying the actual HTML output that Hugo produces and the browser consumes, introducing structured HTML elements, semantic landmarks, accessibility skip links, and DOM inspection.

---

## 🎯 Chapter 4 Goal

Understand the underlying HTML structure of your website:
- Inspect rendered pages using browser developer tools (`F12` or right-click **Inspect**).
- Understand the 4 stages of content: **Content Source** (Markdown) ➔ **Layout Source** (Hugo Go template) ➔ **Generated Static HTML** (Build output/preview response) ➔ **Live DOM** (Browser parsed document).
- Make a persistent, structured HTML change to the shared footer in `layouts/all.html`.
- Learn HTML semantics: `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`.
- Master element attributes: `href`, `src`, `alt`, `id`, `class`, `aria-label`, and `tabindex`.
- Test accessibility features like skip links and diagnose missing fragment targets (`#main` vs `#missing-main`).
- Critically evaluate markup proposed by AI agents.

---

## 📁 What Changed in Chapter 4 (Additive from Chapter 3)

```text
my-knowledge-site/
├── hugo.toml
├── layouts/
│   └── all.html                   # [UPDATED] Replaced plain footer with structured <p> elements,
│                                  #           added class="footer-note" and {{ "about/" | relURL }} link
├── static/css/site.css
└── content/                       # Retains all 7 pages from Chapter 3
    ├── _index.md                  # Home page
    ├── about/
    │   └── index.md               # About page
    ├── articles/
    │   ├── _index.md              # Articles section landing page
    │   └── first-learning-note/   # First article with screenshot
    │       ├── index.md
    │       └── notebook-preview.png
    ├── projects/
    │   ├── _index.md              # Projects section landing page
    │   └── learning-notebook/
    │       └── index.md           # Project description
    └── resources/
        └── index.md               # Curated resources page
```

### The Updated Footer in `layouts/all.html`:
```html
<footer>
  <p>Learn, review &amp; share.</p>
  <p class="footer-note">
    Read <a href="{{ "about/" | relURL }}">about this notebook</a>.
  </p>
</footer>
```

- **Nesting**: The link `<a href="...">` is nested inside `<p class="footer-note">`, which is nested inside `<footer>`.
- **Character Entity**: `&amp;` renders as a literal `&` in the browser.
- **Styling Target**: The class `footer-note` provides a targeted hook for CSS styling in Chapter 5.
- **Dynamic URL**: `{{ "about/" | relURL }}` guarantees the About link resolves correctly whether hosted at the domain root (`/about/`) or a subdirectory.

---

## 🛠️ Key HTML & Architecture Concepts

### 1. The Four Forms of a Page
| Stage | Where it Lives | Example |
| :--- | :--- | :--- |
| **Content Source** | `content/articles/first-learning-note/index.md` | Front matter `title` + Markdown body |
| **Layout Source** | `layouts/all.html` | `<h1>{{ .Title }}</h1>` + `{{ .Content }}` |
| **Generated HTML** | HTTP response from `hugo server` or `public/.../index.html` | Static HTML text delivered to the browser |
| **Live DOM** | Browser Elements / Inspector panel | Parsed Document Object Model in browser RAM |

> **Key Rule**: Editing the DOM inside browser DevTools is temporary. Persistent changes must always be committed to the content Markdown or layout template source files!

### 2. Semantic Elements vs Plain Divs
- `<header>`: Site branding and global navigation.
- `<nav aria-label="Main navigation">`: Navigation links with accessibility labeling.
- `<main id="main" tabindex="-1">`: Primary page content targetable by skip links.
- `<article>`: Self-contained composition (articles, notes).
- `<footer>`: Metadata, copyright, secondary links.

### 3. Attributes Demystified
- **`id`**: Unique identifier on a single page (e.g., `id="main"`). Used as a target for fragment links (`href="#main"`).
- **`class`**: Reusable label shared across multiple elements (e.g., `class="footer-note"`). Used as styling hooks in CSS.
- **`src` & `alt`**: `src` points to the media file; `alt` provides equivalent text for screen readers or when images fail to load. (Purely decorative images use `alt=""`).
- **`tabindex="-1"`**: Allows programmatic focus (e.g., when clicking the skip link) without adding the element to the sequential <kbd>Tab</kbd> cycle.

---

## 🚀 Running the Preview Server

Start the local development server:

```bash
hugo server
```

Open your browser at:
```text
http://localhost:1313/
```

### Guided Developer Tools Exercises:
1. **Open DevTools**: Press <kbd>F12</kbd> (or <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>I</kbd> / <kbd>Cmd</kbd> + <kbd>Option</kbd> + <kbd>I</kbd>).
2. **Temporary DOM Edit**:
   - Double-click the `<h1>` in the Elements panel and change its text to `"A temporary browser edit"`.
   - Hit <kbd>Enter</kbd> to see it change live.
   - Refresh the page (<kbd>F5</kbd>): the original source title reappears!
3. **Trace the Skip Link**:
   - Focus the browser URL bar, press <kbd>Tab</kbd> to reveal the hidden **Skip to content** link, and press <kbd>Enter</kbd>.
   - Notice the URL changes to `#main` and focus jumps directly to `<main id="main">`.

---

## 🧪 Automated Testing

Automated tests for Chapters 1, 2, 3, and 4 are located in the `tests/` directory:

```bash
# Run all chapter tests
python -m unittest discover tests

# Or run Chapter 4 tests specifically
python tests/test_chapter_04.py
```

### What `test_chapter_04.py` Verifies:
1. **Build Success**: Validates that Hugo compiles all templates with zero errors.
2. **Persistent Footer in Layout**: Ensures `layouts/all.html` contains the structured footer, About link, and `footer-note` class.
3. **Site-Wide Footer Presence**: Verifies every generated HTML file contains the new footer markup and character entity `&amp;`.
4. **Skip Link & Target Integrity**: Confirms `<a class="skip-link" href="#main">` matches `<main id="main" tabindex="-1">` across all pages.
5. **Single `<h1>` Outline**: Checks that every page has exactly one `<h1>` element, ensuring a clean semantic document outline.
6. **Semantic Landmarks**: Validates presence of `<header>`, `<nav>`, `<main>`, `<article>`, and `<footer>` on every page.
7. **Void Elements & Image Attributes**: Verifies `<img>` has valid `src` and non-empty `alt`, and ensures no invalid closing tags (e.g., `</img>` or `</meta>`).

---

## ⏩ Next Step: Chapter 5

In **Chapter 5: Practical CSS for Your Hugo Site**, you will use CSS to style your semantic HTML, target the `footer-note` class, design responsive layouts, and create clean typographic hierarchies.
