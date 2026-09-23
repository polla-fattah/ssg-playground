# SSG Playground — Chapter 01: Your First Hugo Website

Welcome to the hands-on playground repository for **Chapter 1** of *Static Site Generators in the Age of AI*.

This branch (`chapter-01`) contains the minimal, working starter project for **My Knowledge Notebook**.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 1 Goal

By the end of this exercise, you should be able to say:
> **"I know which file contains these words, I can change them, and I can put them back."**

---

## 📋 Prerequisites

Before starting, ensure that **Hugo** is installed and accessible in your terminal:

```bash
hugo version
```

> **Note:** You need **Hugo v0.146.0** or later (Extended or Standard edition). For Hugo v0.158.0+, the site configuration uses `locale = 'en'`.

---

## 🚀 How to Run the Website Locally

1. Open your terminal in this project folder (`ssg-playground`).
2. Start the Hugo development preview server:

```bash
hugo server
```

3. Open your browser and navigate to:
   ```text
   http://localhost:1313/
   ```
   *(Or click the link in your VS Code terminal using `Ctrl + Click` / `Cmd + Click`).*

4. To stop the server at any time, click inside the terminal and press `Ctrl + C`.

---

## 📁 Project Structure & Roles

This starter deliberately keeps responsibilities cleanly separated across 4 files:

| File | Role / Purpose | When to edit |
| :--- | :--- | :--- |
| `content/_index.md` | **Page Content & Metadata** | To edit the homepage headings, intro, and lists. |
| `hugo.toml` | **Site Configuration** | To change site-wide settings such as `title` and `locale`. |
| `layouts/all.html` | **HTML Structure** | Supplied layout template combining content with presentation. |
| `static/css/site.css` | **Visual Styling** | Supplied stylesheet controlling fonts, spacing, and colors. |

---

## ✍️ Guided Exercises for Chapter 1

### 1. Personalize Your Introduction
- Open `content/_index.md`.
- Find:
  ```markdown
  Hello! I am Dana. This is where I collect useful ideas, learning notes, and small projects.
  ```
- Replace it with your own name and description.
- Save (`Ctrl + S` / `Cmd + S`) and verify that your browser preview updates immediately without a page reload.

### 2. Change the Page Heading (Front Matter)
- In `content/_index.md`, find the front matter block at the top between `---` lines:
  ```yaml
  ---
  title: "Welcome to my knowledge notebook"
  ---
  ```
- Change the `title` to your own headline (e.g., `title: "Welcome to Sara's learning space"`).
- Save and verify the large heading on the webpage.

### 3. Practice Recovery (Break Something Deliberately)
- Replace your introduction paragraph with:
  ```markdown
  This paragraph was changed by mistake.
  ```
- Save and see the wrong content live in your browser.
- Use **Undo** (`Ctrl + Z` / `Cmd + Z`) in your editor to restore the original text, then save again.
- *Key Takeaway:* A website can build cleanly and still present incorrect information!

### 4. Independent Challenge
- Add one new bullet under `## My interests`.
- Rewrite the sentence under `## Next steps`.
- Check both changes in the browser.

---

## 🛠️ Common Troubleshooting

| Issue | Cause & Fix |
| :--- | :--- |
| **`hugo` command not recognized** | Hugo is not in your system `PATH`. Restart your terminal or VS Code after installing. |
| **Port 1313 is already in use** | An earlier Hugo server is still running. Stop it with `Ctrl+C` or run: `hugo server --port 1314`. |
| **Browser shows connection error** | Check whether `hugo server` was accidentally stopped in your terminal. |
| **Changes don't show in browser** | Ensure you saved the file (`Ctrl+S`) and that the terminal reports no syntax errors. |

---

## 🧪 Automated Tests

You can verify that your Hugo installation, template layout, generated HTML, navigation anchors, and CSS assets all meet the Chapter 1 requirements by running the automated test suite:

```bash
python -m unittest tests/test_chapter_01.py
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.23s

OK
```

---

## ⏭️ What's Next?
In **Chapter 2**, we will add standalone articles, understand Markdown in depth, and link internal pages.
