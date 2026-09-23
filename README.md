# SSG Playground — Chapter 19: Build Your Own Publishing Project

Welcome to the culminating branch for **Chapter 19** of *Static Site Generators in the Age of AI*.

This branch (`chapter-19`) is **additive from `chapter-18`**. It represents the completed, fully-featured reference implementation of the entire book, packaged with a formal project brief (`BRIEF.md`), long-term maintenance commitments (`MAINTENANCE.md`), and updated developer/agent guidance (`AGENTS.md`).

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 19 Goals

- **Synthesize All 18 Chapters**:
  - Understand how all built capabilities work together in harmony:
    - **Publishing & Layout**: Semantic HTML5 base layout, plain CSS with logical properties, partials, section lists, and RSS feeds.
    - **Content Architecture**: Leaf bundles, section landing pages, standardized front matter, and archived statuses.
    - **Data & Discoverability**: Build-time JSON resource directories, client-side substring search, dynamic titles, and metadata fallbacks.
    - **Multilingual Support**: Central Kurdish (Sorani) RTL localization, `i18n` translation keys, language link alternatives, and translation verification dates.
    - **Interactivity & Privacy**: Client-side contact form with mail client handoff and zero remote data retention.
    - **Engineering Rigor**: Pinned dependencies, automated GitHub Actions checks enforcing link hygiene and version parity, and Git revert incident recovery.
- **Formalize the Project Brief (`BRIEF.md`)**:
  - State the project's target **Audience**, **Purpose**, **Success** metrics, and **Content** inventory.
  - Explicitly define **Out of Scope** boundaries (what the site deliberately refuses to do).
  - Categorize all capabilities by their ongoing maintenance costs (**Yes**, **Later**, or **No**).
  - Document **Review and Maintenance** ownership and accountability.
- **Set Long-Term Maintenance Commitments**:
  - Maintain `MAINTENANCE.md` with recurring audit questions and specific calendar review dates.
  - Document the project brief in `AGENTS.md`.

---

## 📁 Repository State at Chapter 19

```text
my-knowledge-site/
├── .github/
│   └── workflows/
│       ├── hugo.yaml                          # Automated deployment to GitHub Pages (pinned HUGO_VERSION)
│       └── checks.yaml                        # Automated PR checks: linting, link hygiene, version parity
├── assets/
│   └── data/
│       └── resource_links.json                # Structured JSON resource directory
├── content/
│   ├── _index.md                              # English home page
│   ├── _index.ckb.md                          # Kurdish home page (RTL)
│   ├── about/                                 # About section (EN + CKB)
│   ├── articles/                              # Learning notes and articles
│   ├── projects/                              # Projects directory (in-progress and archived)
│   ├── resources/                             # Resource directory page
│   ├── search/                                # Progressive-enhancement search page
│   └── contact/                               # Accessible contact page with mailto handoff
├── i18n/
│   ├── en.toml                                # English interface strings
│   └── ckb.toml                               # Kurdish interface strings
├── layouts/
│   ├── baseof.html                            # Master semantic layout with dynamic lang & dir
│   ├── all.html                               # General content layout
│   ├── _partials/                             # Reusable components (meta, resources, footer, language links)
│   ├── projects/                              # Project section layout
│   ├── resources/                             # Resource directory layout
│   ├── search/                                # Search page layout
│   └── contact/                               # Contact form layout
├── static/
│   ├── css/site.css                           # Plain CSS stylesheet with logical properties and RTL support
│   └── js/                                    # Vanilla JS scripts (search.js, contact.js)
├── AGENTS.md                                  # Complete agent working agreements & file map
├── BRIEF.md                                   # Formal project brief & capability evaluation
├── MAINTENANCE.md                             # Scheduled maintenance pass & persistent rules
├── hugo.toml                                  # Modern multilingual Hugo configuration
└── README.md                                  # Complete project documentation
```

---

## 🚀 Running and Testing the Complete Site

### 1. Build and Preview with Hugo
```bash
# Start the local development server
hugo server

# Open the site in your browser:
# http://localhost:1313/my-knowledge-site/
```

### 2. Verify Output and Build Strictness
```bash
# Test the production build with zero warnings permitted
hugo --minify --panicOnWarning
```

### 3. Run the Full Automated Test Suite
Run the comprehensive automated test suite spanning all 19 chapters:
```bash
# Run Chapter 19 validation tests
python -m unittest tests/test_chapter_19.py -v

# Run the complete test suite (Chapters 01 - 19)
python -m unittest discover tests -v
```

---

## 💡 What This Method Delivers
- **True Content Ownership**: Plain Markdown text, standard templates, and plain CSS in folders you own.
- **Inspectable & Auditable**: Every change is visible in Git diffs and reproducible with a single command.
- **Zero Lock-In**: Immune to platform policy shifts, proprietary CMS lock-ins, or uninspected automated regressions.
