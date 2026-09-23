# SSG Playground - Chapter 06: Track and Recover Your Hugo Site with Git

Welcome to the hands-on playground repository for **Chapter 6** of *Static Site Generators in the Age of AI*.

This branch (`chapter-06`) is **additive from `chapter-05`**. It transitions your publishing project from manual sibling backup folders into professional version control using **Git**, tracking source files, staging changes deliberately, writing clear commit messages, and practicing safe recovery techniques.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

##  Chapter 6 Goal

Master the fundamental local Git workflow:
- Understand the 3 Git areas: **Working Tree**  **Staging Area**  **Commit History**.
- Configure `.gitignore` so Hugo build artifacts (`public/`, `resources/`, `.hugo_build.lock`) and operating system files (`.DS_Store`, `Thumbs.db`) stay out of history.
- Stage and record a useful content addition: **My publishing checklist** in `content/articles/first-learning-note/index.md`.
- Make an independent content refinement to `content/about/index.md`.
- Master the difference between:
  - `git restore --staged -- <file>` (removes from next commit, preserves working edits).
  - `git restore -- <file>` (discards working tree edits, restores clean state).
- Read commit logs using `git log --oneline -5` and compare commits with `git diff HEAD~1 HEAD`.

---

##  What Changed in Chapter 6 (Additive from Chapter 5)

```text
my-knowledge-site/
+-- .gitignore                                         # [UPDATED] Exclude /public/, /resources/, .lock, OS files
+-- hugo.toml
+-- layouts/
|   +-- all.html
+-- static/css/site.css
+-- content/
    +-- _index.md
    +-- about/
    |   +-- index.md                                  # [UPDATED] Refined introductory summary (Sec 6.7)
    +-- articles/
    |   +-- _index.md
    |   +-- first-learning-note/
    |       +-- index.md                              # [UPDATED] Added "My publishing checklist" (Sec 6.4)
    |       +-- notebook-preview.png
    +-- projects/
    +-- resources/
```

### 1. Publishing Checklist Added (`content/articles/first-learning-note/index.md`)
```markdown
## My publishing checklist

- Read the page in the local preview.
- Check its links and image description.
- Review the changed files before recording a checkpoint.
```

### 2. Refined Description (`content/about/index.md`)
```markdown
This notebook collects things I am learning and projects I am developing. It is a structured record of practical work with static site generators and web publishing.
```

### 3. Comprehensive `.gitignore` Rules
```gitignore
# Hugo output and generated files
/public/
/resources/
/.hugo_build.lock
/hugo_stats.json

# Local operating-system metadata
.DS_Store
Thumbs.db
```

---

##  The Three Places an Edit Can Be

| Place | Meaning | Key Command |
| :--- | :--- | :--- |
| **Working Tree** | The project files on your disk | Saved in editor |
| **Staging Area** | Prepared contents for the upcoming commit | `git add <file>` |
| **Commit History** | Recorded checkpoints in `.git` repository | `git commit -m "..."` |

### Key Diffs Comparison:
- `git diff -- <file>`: Compares your **Working Tree** with the **Staging Area** (what has been edited but not yet staged).
- `git diff --cached -- <file>`: Compares the **Staging Area** with the **Last Commit** (what is about to be recorded).

---

##  Safe Recovery Exercises

### 1. Unstage Without Losing Work
If you staged a file prematurely and want to review or edit further:
```bash
git restore --staged -- content/articles/first-learning-note/index.md
```
*Result*: The file remains modified in your editor; it is merely removed from the staging index.

### 2. Discard an Unstaged Mistake
If you made a bad edit (e.g. testing `font-size: 6rem;` in `site.css`) and haven't staged it:
```bash
git restore -- static/css/site.css
```
*Result*: The working file is completely restored to the last clean recorded state.

---

##  Automated Testing

Automated tests for Chapters 1 through 6 are in the `tests/` directory:

```bash
# Run all chapter tests
python -m unittest discover tests

# Or run Chapter 6 tests specifically
python tests/test_chapter_06.py
```

### What `test_chapter_06.py` Verifies:
1. **Hugo Build**: Validates compilation with exit code 0.
2. **Publishing Checklist in Source**: Confirms `## My publishing checklist` and all 3 checklist items exist in `first-learning-note/index.md`.
3. **Publishing Checklist in Output**: Confirms the generated HTML renders the checklist heading and list items.
4. **Git Ignore Integrity**: Confirms `.gitignore` properly ignores `/public/`, `/resources/`, lock files, and OS thumbnails.
5. **About Page Refinement**: Checks that the About page contains the independent improvement.
6. **Git Branch & Repository Status**: Verifies the repository status on branch `chapter-06`.

---

##  Next Step: Chapter 7

In **Chapter 7: Publish Your Hugo Site with GitHub Pages**, you will connect your local Git repository to GitHub and set up an automated CI/CD GitHub Actions workflow to publish your site live on the web!
