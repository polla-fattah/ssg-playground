# SSG Playground - Chapter 16: Publish in Multiple Languages

Welcome to the hands-on playground repository for **Chapter 16** of *Static Site Generators in the Age of AI*.

This branch (`chapter-16`) is **additive from `chapter-15`**. It guides you through configuring Hugo's multilingual engine, internationalizing interface strings with `i18n`, supporting Right-to-Left (RTL) writing directions using CSS logical properties, creating translated content files, rendering language link alternatives, and maintaining translations over time with verification dates and CI checks.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

##  Chapter 16 Goals

- **Configure Multilingual Support in `hugo.toml`**:
  - Set `defaultContentLanguage = 'en'` and `defaultContentLanguageInSubdir = false`.
  - Define language blocks under `[languages.en]` and `[languages.ckb]`.
  - Configure modern Hugo language parameters:
    - `locale` (`'en'`, `'ckb'`)
    - `label` (`'English'`, `''`)
    - `direction` (`'rtl'` for Kurdish/CKB)
    - `title` per language.
- **Dynamic Language & Direction in Base Layout**:
  - Update `layouts/baseof.html` with:
    ```html
    <html lang="{{ .Site.Language.Locale }}" dir="{{ .Site.Language.Direction | default "ltr" }}">
    ```
  - Ensure the browser automatically knows document language and reading direction for correct text flow and screen reader pronunciation.
- **Externalize Interface Strings (`i18n`)**:
  - Replace hardcoded UI strings with `{{ i18n "key" }}` in templates.
  - Create string lookup tables in `i18n/en.toml` and `i18n/ckb.toml` with complete key parity across:
    - Skip link (`skip_to_content`)
    - Navigation items (`nav_home`, `nav_about`, `nav_articles`, `nav_projects`, `nav_resources`, `nav_search`)
    - Footer tagline (`footer_tagline`)
  - Use `relLangURL` instead of `relURL` so navigation links preserve the current language prefix (`/ckb/...`).
- **Language Switcher Partial**:
  - Create `layouts/_partials/language-links.html`.
  - Render links to translated versions of the current page using `.Translations`:
    ```html
    {{ if .IsTranslated }}
      <p class="language-links">
        {{ range .Translations }}
          <a href="{{ .RelPermalink }}" hreflang="{{ .Language.Locale }}" lang="{{ .Language.Locale }}" rel="alternate">{{ .Language.Label }}</a>
        {{ end }}
      </p>
    {{ end }}
    ```
  - Include the partial in the `<header>` element of `layouts/baseof.html`.
- **Bidirectional CSS & Logical Properties**:
  - Replace physical positioning in `static/css/site.css`:
    - Changed `.skip-link { left: 1rem; }` to `inset-inline-start: 1rem;`.
  - Add typography adjustment for Central Kurdish:
    ```css
    :lang(ckb) {
      line-height: 1.9;
    }
    ```
  - Add styles for `.language-links`.
- **Parallel Content Translation & Maintenance**:
  - Create `content/_index.ckb.md` and `content/about/index.ckb.md`.
  - Include front matter field `source_checked: "YYYY-MM-DD"` indicating when the translation was verified against the English original.
  - Update CI checks in `.github/workflows/checks.yaml` to ensure every `*.ckb.md` file contains a non-empty `source_checked:` field.
  - Update `AGENTS.md` with guidelines on language codes, translation file locations, and verification tracking.

---

##  What Changed in Chapter 16 (Additive from Chapter 15)

```text
my-knowledge-site/
+-- hugo.toml                                  # [UPDATED] Configured [languages.en] and [languages.ckb] with locale, label, direction
+-- layouts/
|   +-- baseof.html                            # [UPDATED] Added dynamic lang/dir, i18n calls, relLangURL, and language-links partial
|   +-- _partials/
|       +-- footer.html                        # [UPDATED] Language-aware about link (relLangURL) and i18n tagline
|       +-- language-links.html                # [NEW] Alternate language links switcher using .Translations
+-- i18n/
|   +-- en.toml                                # [NEW] English interface strings
|   +-- ckb.toml                               # [NEW] Kurdish (Sorani) interface strings
+-- content/
|   +-- _index.ckb.md                          # [NEW] Kurdish home page with source_checked metadata
|   +-- about/
|       +-- index.ckb.md                       # [NEW] Kurdish About page with source_checked metadata
+-- static/
|   +-- css/
|       +-- site.css                           # [UPDATED] CSS logical property (inset-inline-start), :lang(ckb) line-height, .language-links
+-- .github/
|   +-- workflows/
|       +-- checks.yaml                        # [UPDATED] Added CI check 4 for source_checked in Kurdish content files
+-- AGENTS.md                                  # [UPDATED] Added multilingual structure, translation guidelines, and maintenance policy
```

---

##  Running and Testing Locally

### 1. Build and Preview with Hugo
```bash
# Preview the site locally (both English and Kurdish pages)
hugo server

# Preview English at:
# http://localhost:1313/my-knowledge-site/

# Preview Kurdish at:
# http://localhost:1313/my-knowledge-site/ckb/
```

### 2. Verify Output and Build Strictness
```bash
# Build the site and fail immediately on any warning or deprecation
hugo --minify --panicOnWarning
```

### 3. Run Automated Validation Tests
Run all chapter test suites to ensure both additive features and backward compatibility pass:
```bash
# Run Chapter 16 validation suite
python -m unittest tests/test_chapter_16.py -v

# Run the complete test suite (Chapters 01 - 16)
python -m unittest discover tests -v
```

---

##  Key Concepts Explained

### 1. Modern Hugo Language Keys
Hugo v0.158+ introduced standardized configuration keys for multilingual sites:
- `locale` replaces `languageCode` (e.g. `en`, `ckb`)
- `label` replaces `languageName` (e.g. `English`, ``)
- `direction` replaces `languageDirection` (e.g. `ltr`, `rtl`)

In templates, access these using:
- `.Site.Language.Locale`
- `.Site.Language.Direction`
- `.Language.Label` / `.Language.Locale` (inside `.Translations` iteration)

### 2. Physical vs. Logical CSS Properties
In multilingual websites with mixed text directions (LTR and RTL), hardcoding directional properties creates layout bugs in RTL mode:
- `left: 1rem` $\rightarrow$ `inset-inline-start: 1rem`
- `margin-right: 0.5rem` $\rightarrow$ `margin-inline-end: 0.5rem`
- `text-align: left` $\rightarrow$ `text-align: start`

Browsers automatically flip logical properties based on the element's effective `dir` attribute (`dir="rtl"` vs. `dir="ltr"`).

### 3. Maintenance Tracking (`source_checked`)
Translations easily drift out of date when source content changes. Tracking the verification date directly in the translated page's front matter:
```markdown
---
title: "  "
source_checked: "2026-09-17"
---
```
enables automated verification in CI pipelines, ensuring no untracked translations linger without a known audit date.
