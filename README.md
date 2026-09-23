# SSG Playground — Chapter 14: Check Every Contribution with CI/CD

Welcome to the hands-on playground repository for **Chapter 14** of *Static Site Generators in the Age of AI*.

This branch (`chapter-14`) is **additive from `chapter-13`**. It introduces Continuous Integration (CI) with GitHub Actions to test proposed changes on branches and pull requests before they can be merged into `main` and published to the live site.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 14 Goals

- **Separate Checking from Deploying**:
  - Keep the deployment workflow (`.github/workflows/hugo.yaml`) untouched, triggered only on `push` to `main`.
  - Add a dedicated checks workflow (`.github/workflows/checks.yaml`) triggered on `pull_request` to `main`.
- **Enforce Narrow Permissions**:
  - The checks workflow runs with `contents: read` only (reporting results).
  - It does NOT have `pages: write` or `id-token: write`, ensuring an unverified proposal cannot deploy.
- **Enforce the Three Established Repository Rules**:
  1. *Directory flags are Booleans*: `start_here` in `assets/data/resource_links.json` must be an unquoted Boolean (`true` or `false`), catching the Chapter 12 pitfall where quoted `"false"` was truthy in Hugo templates.
  2. *Internal links stay relative*: Markdown links in `content/` must not use root-relative `](/' paths, catching the Chapter 8 baseURL prefix pitfall.
  3. *Articles and projects have descriptions*: All page bundles under `content/articles/*/index.md` and `content/projects/*/index.md` must have a non-empty `description:` field in front matter.
- **Run Checks Locally First**:
  - Execute the checks directly in the local terminal before pushing:
    ```bash
    hugo --minify --panicOnWarning
    grep -n '"start_here": *"' assets/data/resource_links.json
    grep -rn '](/' content/
    grep -c '^description:' content/articles/*/index.md content/projects/*/index.md
    ```
- **Raise Content Rather Than Weakening Rules**:
  - When the new check identifies that `content/articles/first-learning-note/index.md` (written in Chapter 2) lacks a `description`, add the missing description rather than exempting older content.
- **Branch and Pull Request Lifecycle**:
  - Propose changes on branch `add-actions-resource` using `git switch -c`.
  - Add the 5th resource record ("GitHub: Actions documentation") to `assets/data/resource_links.json`.
  - Open a pull request using GitHub Web or GitHub CLI (`gh pr create`).
- **Designed Failure Experiment**:
  - Intentionally quote `"start_here": "false"` to observe the check turn red and stop the PR.
  - Read the log from the top to isolate the failing rule.
  - Repair the boolean (`start_here: false`), push, observe green check, and merge.
- **What Checks Can and Cannot Establish**:
  - *Machines check*: Syntax, template rendering without warnings, boolean types, link formats, and field existence.
  - *Humans check*: Truthfulness, accuracy, source validity, and whether a resource or page is suitable for publication.

---

## 📁 What Changed in Chapter 14 (Additive from Chapter 13)

```text
my-knowledge-site/
├── .github/
│   └── workflows/
│       ├── hugo.yaml                          # [From Chapter 7] CD deployment workflow (triggers on push to main)
│       └── checks.yaml                        # [NEW] CI checking workflow (triggers on pull_request to main)
├── content/
│   └── articles/
│       └── first-learning-note/
│           └── index.md                       # [UPDATED] Added front matter description to satisfy CI check
├── assets/
│   └── data/
│       └── resource_links.json                # [UPDATED] Added 5th record for GitHub Actions documentation
├── sources/
│   └── publishing-notes.md                    # [From Chapter 13] Raw working notes
├── AGENTS.md                                  # [From Chapter 13] Guidance and working agreements
├── layouts/                                   # [From Chapter 11 & 12] Baseof, layouts, and data partials
├── static/                                    # [From Chapter 5] Site styling
└── tests/
    ├── test_chapter_01.py ... test_chapter_13.py
    └── test_chapter_14.py                     # [NEW] Automated tests for workflow schema, rules, and 5th record
```

---

## ⚙️ The Checks Workflow (`.github/workflows/checks.yaml`)

```yaml
name: Check proposed changes

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  checks:
    runs-on: ubuntu-24.04
    env:
      HUGO_VERSION: "0.150.0"
    steps:
      - name: Check out the proposed source
        uses: actions/checkout@v7

      - name: Install Hugo
        shell: bash
        run: |
          curl --fail --location --retry 3 \
            --output "$RUNNER_TEMP/hugo.tar.gz" \
            "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_linux-amd64.tar.gz"
          mkdir -p "$RUNNER_TEMP/hugo-bin"
          tar -xzf "$RUNNER_TEMP/hugo.tar.gz" -C "$RUNNER_TEMP/hugo-bin" hugo
          echo "$RUNNER_TEMP/hugo-bin" >> "$GITHUB_PATH"

      - name: Build the website
        run: hugo --minify --panicOnWarning

      - name: Check that directory flags are Booleans
        shell: bash
        run: |
          if grep -n '"start_here": *"' assets/data/resource_links.json; then
            echo "start_here must be an unquoted Boolean: true or false."
            exit 1
          fi

      - name: Check that internal links stay relative
        shell: bash
        run: |
          if grep -rn '](/' content/; then
            echo "Internal links must be relative, not root-relative."
            exit 1
          fi

      - name: Check that articles and projects have a description
        shell: bash
        run: |
          status=0
          for page in content/articles/*/index.md content/projects/*/index.md; do
            if ! grep -q '^description:' "$page"; then
              echo "Missing description: $page"
              status=1
            fi
          done
          exit "$status"
```

---

## 📋 The 5th Resource Record (`assets/data/resource_links.json`)

```json
  {
    "title": "GitHub: Actions documentation",
    "url": "https://docs.github.com/en/actions",
    "description": "The official reference for automating builds, checks, and deployments on GitHub.",
    "topics": ["GitHub Actions", "Automation"],
    "start_here": false
  }
```

---

## 🧪 Testing & Verification

Run the automated test suite across all chapters:

```bash
# Run unit tests across all chapters (Chapters 01 through 14)
python -m unittest discover tests

# Build site with strict checks
hugo --minify --panicOnWarning

# Local preview server
hugo server
```

All 86 test assertions should pass cleanly.
