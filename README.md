# SSG Playground - Chapter 18: Maintain, Migrate, and Recover

Welcome to the hands-on playground repository for **Chapter 18** of *Static Site Generators in the Age of AI*.

This branch (`chapter-18`) is **additive from `chapter-17`**. It addresses long-term site health, ongoing maintenance routines, automated dependency synchronization across GitHub workflows, graceful content retirement without URL breakage, and disciplined incident recovery using Git history.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

##  Chapter 18 Goals

- **Run a Repeatable Maintenance Pass**:
  - Periodically audit:
    1. Statements about project progress and stale claims.
    2. Translation currency using `source_checked` front matter dates.
    3. Live URL resolution across all published pages.
    4. Alignment of Hugo versions across CI/CD workflows and local machines.
    5. Accuracy of `AGENTS.md` and repository guidelines.
- **Workflow Dependency Synchronization**:
  - Keep `HUGO_VERSION` identical across:
    - `.github/workflows/hugo.yaml`
    - `.github/workflows/checks.yaml`
  - Add a 5th automated check to `.github/workflows/checks.yaml` verifying that both workflows pin the exact same Hugo version, preventing drift where PR checks test a different version than the publishing workflow deploys.
- **Retire Content Without Breaking Addresses**:
  - Understand why deleting published pages or setting `draft: true` creates silent 404 damage for readers.
  - Archive superseded pages gracefully:
    - Set `params.status: "archived"`.
    - Keep `draft: false`.
    - Add an explicit banner notice in the page body explaining where the work moved.
  - Test and verify Hugo's `aliases` mechanism for permanent URL redirects.
- **Incident Recovery with `git revert`**:
  - Learn why `git reset --hard` and forced pushes are dangerous on published repositories.
  - Use `git revert` (or `git revert -m 1` on merge commits) to create forward-moving commits that undo mistakes while preserving a truthful audit trail.
- **Backups, Credentials, and Platform Ownership**:
  - Differentiate between a collaborative remote (`origin`) and an independent backup (`git clone --mirror`).
  - Never commit secrets or API tokens to Git. If committed, revoke immediately at the service.
  - Document routines, decisions, and agreements in `MAINTENANCE.md`.

---

##  What Changed in Chapter 18 (Additive from Chapter 17)

```text
my-knowledge-site/
+-- .github/
|   +-- workflows/
|       +-- checks.yaml                        # [UPDATED] Added check 5: Hugo version parity across workflows
+-- content/
|   +-- projects/
|       +-- reading-list/
|           +-- index.md                       # [UPDATED] Archived status and notice pointing to Resources page
+-- AGENTS.md                                  # [UPDATED] Added MAINTENANCE.md reference & archiving working agreement
+-- MAINTENANCE.md                             # [NEW] Recurring maintenance routine & persistent project decisions
+-- README.md                                  # [UPDATED] Chapter 18 guide and testing instructions
```

---

##  Running and Testing Locally

### 1. Build and Preview with Hugo
```bash
# Preview the site locally
hugo server

# Verify archived project display:
# http://localhost:1313/my-knowledge-site/projects/
# http://localhost:1313/my-knowledge-site/projects/reading-list/
```

### 2. Verify Output and Build Strictness
```bash
# Build the site and panic immediately on any warning or deprecation
hugo --minify --panicOnWarning
```

### 3. Run Automated Validation Tests
Run all chapter test suites to ensure both additive features and backward compatibility pass:
```bash
# Run Chapter 18 validation suite
python -m unittest tests/test_chapter_18.py -v

# Run the complete test suite (Chapters 01 - 18)
python -m unittest discover tests -v
```

---

##  Key Architectural Lessons

### 1. Archiving vs. Unpublishing
- `draft: true` tells Hugo: "Do not generate this page in production."
  - Using it on an already-published page removes the file from `public/`, breaking external links, bookmarks, and search index results with 404 errors.
  - Because Hugo's dynamic templates automatically exclude drafts, the broken page also vanishes from section lists without a trace-creating invisible damage.
- `status: "archived"` with `draft: false` tells the reader and templates: "This page still exists at its permanent address for historical truth, but its content is superseded."

### 2. Three Undoing Strategies
| Command | Action | When to use |
| --- | --- | --- |
| `git restore <file>` | Discards uncommitted working tree changes | Before committing. |
| `git reset --hard` | Rewrites commit history backwards | Only on local, unpublished branches that have never been pushed. |
| `git revert <commit>` | Commits the inverse diff forward | Always on published branches (`main`) to preserve a truthful history without breaking collaborators' clones. |
