# SSG Playground - Chapter 07: Publish Your Hugo Site with GitHub Pages

Welcome to the hands-on playground repository for **Chapter 7** of *Static Site Generators in the Age of AI*.

This branch (`chapter-07`) is **additive from `chapter-06`**. It takes your locally tracked Hugo website and publishes it live to the web using **GitHub Pages** powered by an automated **GitHub Actions** CI/CD deployment pipeline.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 7 Goal

Publish your Hugo website to a public, global address:
- Connect your local Git repository to a remote repository on **GitHub**.
- Authenticate seamlessly using the GitHub CLI (`gh auth login --scopes workflow`).
- Configure the public site `baseURL` in `hugo.toml`.
- Set up an automated CI/CD pipeline using `.github/workflows/hugo.yaml` to build and deploy your site on every push to `main`.
- Add the final item to your publishing checklist: **"Check the published page after deployment"**.
- Distinguish between your source code repository, local preview, and live public website.
- Practice diagnosing failed builds locally with `hugo --minify --panicOnWarning` without publishing mistakes.

---

## 📁 What Changed in Chapter 7 (Additive from Chapter 6)

```text
my-knowledge-site/
+-- .github/
|   +-- workflows/
|       +-- hugo.yaml                          # [NEW] Automated GitHub Actions build & deploy workflow
+-- hugo.toml                                  # [UPDATED] Configured baseURL for GitHub Pages
+-- content/
|   +-- articles/
|       +-- first-learning-note/
|           +-- index.md                       # [UPDATED] Added 4th publishing checklist item
+-- layouts/
+-- static/
+-- tests/
    +-- test_chapter_07.py                     # [NEW] Automated validation tests for Chapter 7
```

---

## ⚙️ The GitHub Actions Workflow (`.github/workflows/hugo.yaml`)

```yaml
name: Publish Hugo site

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-24.04
    env:
      HUGO_VERSION: "0.150.0"
    steps:
      - name: Check out the source
        uses: actions/checkout@v7

      - name: Read the Pages configuration
        id: pages
        uses: actions/configure-pages@v6

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
        env:
          PAGES_BASE_URL: ${{ steps.pages.outputs.base_url }}
        run: hugo --minify --panicOnWarning --baseURL "${PAGES_BASE_URL}/"

      - name: Upload the generated website
        uses: actions/upload-pages-artifact@v5
        with:
          path: public

  deploy:
    needs: build
    runs-on: ubuntu-24.04
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Publish to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

### Key Highlights of the Pipeline:
1. **Automated Trigger**: Every `git push` to `main` starts a build.
2. **Quality Gate (`--panicOnWarning`)**: Hugo halts the build if any syntax, template, or configuration warning occurs.
3. **Artifact Hand-off**: The `build` job passes the compiled `public/` directory artifact to the secure `deploy` job.
4. **Resilient Hosting**: If a new commit breaks the build, GitHub Actions aborts before deployment, keeping your last working website live online!

---

## 🌐 The Three Core Addresses

| Address Type | Example | Purpose |
| :--- | :--- | :--- |
| **Source Repository** | `https://github.com/YOUR-USERNAME/my-knowledge-site` | Inspect code, issues, and workflow runs |
| **Published Website** | `https://YOUR-USERNAME.github.io/my-knowledge-site/` | Public live website for readers |
| **Local Preview** | `http://localhost:1313/my-knowledge-site/` | Safe editing and verification sandbox |

---

## 🚀 The Complete Publishing Loop

For every future change:
1. **Edit**: Modify Markdown, layout, or CSS locally.
2. **Preview**: Run `hugo server` and inspect the rendered result.
3. **Review**: Use `git status` and `git diff` to check changes.
4. **Commit**: Record a clean commit (`git commit -m "..."`).
5. **Push**: Send to GitHub (`git push`).
6. **Watch**: Observe the Actions workflow succeed.
7. **Verify**: Check the live site at `https://YOUR-USERNAME.github.io/my-knowledge-site/`.

---

## 🧪 Automated Testing

Automated tests for Chapters 1 through 7 are in the `tests/` directory:

```bash
# Run all chapter tests
python -m unittest discover tests

# Or run Chapter 7 tests specifically
python tests/test_chapter_07.py
```

### What `test_chapter_07.py` Verifies:
1. **Production Build**: Compiles site with `hugo --minify --panicOnWarning` with zero errors.
2. **Workflow Configuration**: Confirms `.github/workflows/hugo.yaml` exists and defines correct triggers, permissions, jobs, and actions.
3. **Publishing Checklist in Source**: Verifies `first-learning-note/index.md` contains all 4 publishing checklist items.
4. **Publishing Checklist in HTML**: Verifies rendered HTML includes all 4 checklist items.
5. **Configured baseURL**: Ensures `hugo.toml` contains a valid project-site `baseURL`.

---

## ⏩ Next Step: Chapter 8

In **Chapter 8: Work with an AI Agent on Your Hugo Site**, you will invite an AI coding assistant into your development environment to generate content, audit structure, and collaborate safely under version control!
