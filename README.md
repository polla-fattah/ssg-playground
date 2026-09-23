# SSG Playground - Chapter 13: Create and Maintain Content with AI Agents

Welcome to the hands-on playground repository for **Chapter 13** of *Static Site Generators in the Age of AI*.

This branch (`chapter-13`) is **additive from `chapter-12`**. It demonstrates a disciplined, human-in-the-loop workflow for producing and maintaining content using AI agents. Rather than asking an agent for ungrounded generation, you supply source notes, agree on an article model, request a plan before a draft, check every claim against the source material, and coordinate updates across multiple site files.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 13 Goals

- **Separate Delegation from Human Decisions**:
  - *Delegate*: Ordering rough notes into prose, applying an agreed article structure, writing descriptions, formatting links and JSON records.
  - *Keep with the author*: Deciding whether an event happened, verifying whether a claim is supported, assessing readiness, and deciding publication.
- **Supply Source Material Safely**:
  - Keep source notes in `sources/publishing-notes.md` (outside `content/`), ensuring Hugo never compiles or publishes raw notes.
  - Distinguish author-recorded events, external references, and explicit gaps ("Not" lines).
- **Enforce an Explicit Article Model**:
  - Front matter: `title`, `description` (one sentence), `draft` (`true` until reviewed).
  - Body headings in exact order:
    1. `## What this is about` (2-3 sentences explaining why the article exists)
    2. `## What happened` (sequence of events drawn strictly from sources)
    3. `## What I would do differently` (specific changes or honest unknowns)
    4. `## Sources` (visible Markdown links with short explanatory annotations)
- **Record Working Agreements in `AGENTS.md`**:
  - Direct the agent to use only named source files (no ungrounded generation or web search).
  - Explicitly mandate reporting gaps as unknown rather than inventing estimates.
  - Require visible Markdown attribution in the body rather than hidden front matter.
- **Decompose into Three Reviewable Requests**:
  1. *Plan first (read-only)*: Map proposed claims to specific lines of notes and identify gaps.
  2. *Draft from source only*: Write the article page bundle at `draft: true` under 400 words.
  3. *Coordinated update*: Link the new article from `content/articles/_index.md`, `content/_index.md`, and add the cited reference to `assets/data/resource_links.json`.
- **Review for Meaning vs Technical Build Success**:
  - Test the "designed failure": adding an unsupported claim (`"Deployments usually finish in under a minute."`) passes `hugo --minify --panicOnWarning` without error.
  - Understand why automated checks verify only templates and syntax, while human review must verify factual accuracy against sources.
- **Deliberate Publication**:
  - Explicitly toggle `draft: false` only after human verification.
  - Stage and commit the four coordinated files cleanly.

---

## 📁 What Changed in Chapter 13 (Additive from Chapter 12)

```text
my-knowledge-site/
+-- sources/
|   +-- publishing-notes.md                    # [NEW] Raw working notes from Chapters 6 & 7 (outside content/)
+-- content/
|   +-- articles/
|   |   +-- _index.md                          # [UPDATED] Added link to publishing-with-github-pages/
|   |   +-- publishing-with-github-pages/
|   |       +-- index.md                       # [NEW] Agent-drafted article bundle adhering to the 4-part model
|   +-- _index.md                              # [UPDATED] Added new article link to Latest writing list
+-- assets/
|   +-- data/
|       +-- resource_links.json                # [UPDATED] Added 4th record for GitHub Pages publishing documentation
+-- AGENTS.md                                  # [UPDATED] Added sources/, article paths, and sourcing agreements
+-- layouts/                                   # [From Chapter 11 & 12] Baseof, layouts, and JSON data partials
+-- static/                                    # [From Chapter 5] Site styling
+-- tests/
    +-- test_chapter_01.py ... test_chapter_12.py
    +-- test_chapter_13.py                     # [NEW] Validation tests for sourcing, article structure, and site links
```

---

## 📝 The Agreed Article Model

Located at `content/articles/publishing-with-github-pages/index.md`:

```markdown
---
title: "What I learned publishing with GitHub Pages"
description: "How this notebook reached a public address, and what went wrong the first time."
draft: false
---

## What this is about

This notebook is published from its own repository rather than uploaded by
hand. Setting that up went wrong once, in a way that was easy to misread.

## What happened

A Pages site has to be told where its content comes from. I chose the GitHub
Actions route rather than publishing from a branch, so a workflow builds the
site with Hugo and deploys the built output. The generated `public/` folder is
never committed.

The first deployment failed, because I pushed before setting the publishing
source. Setting it and running the workflow again fixed it. The failure was
only legible in the Actions log; the browser showed a missing page, which told
me nothing about the cause.

One configuration detail mattered more than I expected: `baseURL` has to
include the repository path. Before I corrected it, the live site loaded
without its stylesheet and its internal links went to the wrong place.

I also learned to distrust a passing local build as evidence about the live
site. `hugo --minify --panicOnWarning` succeeded before the push that failed
to deploy.

## What I would do differently

I would set the publishing source before the first push, and read the Actions
log before looking at the site in a browser.

I have not measured how long a deployment usually takes, and I have not tried
a custom domain, so I cannot say anything useful about either.

## Sources

- [GitHub: configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site): Explains how a Pages site is told where to publish from, including the GitHub Actions route used here.
```

---

## 🔄 Coordinated Updates

Connecting the article to the rest of the site requires updating three files:

1. **`content/articles/_index.md`** (Relative link within articles section):
   ```markdown
   - [What I learned publishing with GitHub Pages](publishing-with-github-pages/): Setting up a publishing source, and the first deployment that failed.
   ```

2. **`content/_index.md`** (Relative link from site root):
   ```markdown
   - [What I learned publishing with GitHub Pages](articles/publishing-with-github-pages/)
   ```

3. **`assets/data/resource_links.json`** (Appended 4th record):
   ```json
   {
     "title": "GitHub: configuring a publishing source",
     "url": "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site",
     "description": "The official explanation of how a GitHub Pages site is told where its content is published from.",
     "topics": ["GitHub Pages", "Publishing"],
     "start_here": false
   }
   ```

---

## 🧪 Testing & Verification

Run the automated test suite across all chapters:

```bash
# Run unit tests across all chapters (Chapters 01 through 13)
python -m unittest discover tests

# Build site with strict checks
hugo --minify --panicOnWarning

# Local preview server
hugo server
```

All 80 test assertions should pass cleanly.
