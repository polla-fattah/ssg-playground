# SSG Playground - Chapter 05: Practical CSS for Your Hugo Site

Welcome to the hands-on playground repository for **Chapter 5** of *Static Site Generators in the Age of AI*.

This branch (`chapter-05`) is **additive from `chapter-04`**. It focuses on practical, maintainable CSS styling for your Hugo website-connecting HTML semantic markup to visual presentation, adjusting typography and spacing, understanding the box model, and recognizing responsive design patterns.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 5 Goal

Gain practical CSS literacy to style your site and evaluate code suggested by AI agents:
- Understand where CSS belongs in Hugo: `static/css/site.css` copied directly to `public/css/site.css` (served at `/css/site.css`).
- Style the footer note created in Chapter 4 using the `.footer-note` class selector.
- Improve typography readability by setting `font-size: 1.125rem` on the `body`.
- Create clear vertical visual rhythm by increasing `margin-top: 2.5rem` on `h2` headings.
- Understand the **Box Model** (Margin, Border, Padding, Content) and `box-sizing: border-box`.
- Recognize built-in responsive rules (Flexbox navigation wrapping, max-width constraints, fluid images).
- Diagnose selector mistakes using browser developer tools.
- Preserve accessibility essentials: the `:focus-visible` outline and skip-link styles.

---

## 📁 What Changed in Chapter 5 (Additive from Chapter 4)

In this chapter, **only one file is modified**: `static/css/site.css`.

```text
my-knowledge-site/
+-- hugo.toml
+-- layouts/
|   +-- all.html                   # Unchanged (from Chapter 4)
+-- content/                       # Unchanged (all 7 pages from Chapter 3 & 4)
+-- static/
    +-- css/
        +-- site.css               # [UPDATED] 3 targeted styling additions:
                                   #   1. body { font-size: 1.125rem; }
                                   #   2. h2 { margin-top: 2.5rem; }
                                   #   3. .footer-note { ... }
```

### The Three CSS Updates:

#### 1. Body Font Sizing (`static/css/site.css`)
```css
body {
  margin: 0;
  background: #f5f3ed;
  color: #263238;
  font-family: system-ui, sans-serif;
  font-size: 1.125rem; /* ~18px for comfortable reading */
  line-height: 1.7;
}
```

#### 2. Heading Separation (`static/css/site.css`)
```css
h2 {
  margin-top: 2.5rem; /* Clearer visual separation between sections */
  line-height: 1.3;
}
```

#### 3. Targeted Footer Note Styling (`static/css/site.css`)
```css
.footer-note {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #c5ccce;
  color: #46545b;
}
```

---

## 🎨 Core CSS Concepts for Hugo Authors

### 1. Where CSS Lives in Hugo
| File Path | Role | Public URL |
| :--- | :--- | :--- |
| `static/css/site.css` | **Source stylesheet** you edit | `http://localhost:1313/css/site.css` |
| `public/css/site.css` | **Generated copy** copied at build | *(Never edit this directly!)* |

Hugo serves everything inside `static/` from the root of the site. In `layouts/all.html`, the stylesheet is referenced via:
```html
<link rel="stylesheet" href="{{ "css/site.css" | relURL }}">
```

### 2. The Box Model in Action
- **Margin**: Space *outside* the element's border (`margin-top: 0.75rem`).
- **Border**: Line *around* the element (`border-top: 1px solid #c5ccce`).
- **Padding**: Space *between* the content and border (`padding-top: 0.75rem`).
- **`box-sizing: border-box`**: Ensures padding and borders are included within any declared widths.

### 3. Responsive Features Already Built-In
- **Container Constraint**:
  ```css
  header, main, footer {
    width: min(100% - 2rem, 48rem);
    margin-inline: auto;
  }
  ```
  Prevents uncomfortably long lines on wide desktop monitors while leaving breathing room on mobile screens.
- **Flexbox Navigation**:
  ```css
  nav {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  ```
  Items wrap smoothly onto a new line if the browser window narrows.
- **Responsive Images**:
  ```css
  article img {
    display: block;
    max-width: 100%;
    height: auto;
  }
  ```
  Ensures images never overflow the reading container.

---

## 🚀 How to Run and Test

Start the preview server:
```bash
hugo server
```

Open:
```text
http://localhost:1313/
```

### Guided Exercises:
1. **Inspect the Footer**:
   - Right-click the footer note and select **Inspect**.
   - Notice the **Box Model** diagram in DevTools showing the `margin-top` outside the border and `padding-top` inside.
2. **Test Responsive Layout**:
   - Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd> (<kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd> on macOS) to toggle Device Emulation.
   - Resize to mobile width (360px) and verify navigation wraps cleanly without horizontal overflow.
3. **Keyboard Focus Check**:
   - Press <kbd>Tab</kbd> repeatedly. Ensure the link outline defined in `a:focus-visible` is clearly visible.

---

## 🧪 Automated Testing

Automated tests for Chapters 1 through 5 are in the `tests/` directory:

```bash
# Run all chapter tests
python -m unittest discover tests

# Or run Chapter 5 tests specifically
python tests/test_chapter_05.py
```

### What `test_chapter_05.py` Verifies:
1. **Build Success**: Hugo compiles the site cleanly.
2. **Static Asset Pipeline**: Verifies `static/css/site.css` is faithfully published to `public/css/site.css`.
3. **Typography Rule**: Validates `body` contains `font-size: 1.125rem` and `line-height: 1.7`.
4. **Heading Spacing**: Checks `h2` has `margin-top: 2.5rem`.
5. **Class Selector Rule**: Verifies `.footer-note` styling declarations exist.
6. **Responsive & Accessibility Preservation**: Ensures `min(100% - 2rem, 48rem)`, `flex-wrap: wrap`, `:focus-visible`, and image constraints remain intact.
7. **HTML Linking**: Ensures all 7 pages link to `css/site.css`.

---

## ⏩ Next Step: Chapter 6

In **Chapter 6: Track and Recover Your Hugo Site with Git**, you will move beyond manual folder backups and use Git version control to stage, commit, branch, and inspect history professionally.
