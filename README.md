# SSG Playground - Chapter 17: Add Interactive Features Responsibly

Welcome to the hands-on playground repository for **Chapter 17** of *Static Site Generators in the Age of AI*.

This branch (`chapter-17`) is **additive from `chapter-16`**. It addresses interactivity on a static site by building an accessible contact form, demonstrating why native form submission fails without a server backend, and implementing a client-side mailto handoff that protects visitor privacy by sending zero data to external servers.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 17 Goals

- **Map Where Work Happens**:
  - Understand the three execution environments for web features:
    1. **Build time** (Hugo generating static files, cost-free, reliable, secure)
    2. **Visitor's browser** (JavaScript running locally on the page)
    3. **Someone else's server** (backend functions or third-party APIs with privacy and maintenance costs)
- **Accessible Form Markup**:
  - Build `layouts/contact/page.html` with explicit `<label for="...">` associations matching input `id` attributes.
  - Use semantic input controls (`type="text"`, `<textarea rows="6">`, `required`, `autocomplete="name"`).
  - Use `novalidate` to manage validation messaging cleanly in custom script while retaining standard keyboard navigation and accessibility semantics.
  - Include live feedback container with `role="status"` (`#contact-status`).
- **Demonstrate Static Site Limitations**:
  - Experience the "designed failure": submitting a standard `<form>` without an action re-serves the same static file, loses entered text, and can leak sensitive input into URL query parameters in browser history.
- **Client-Side Validation & `mailto:` Handoff**:
  - Implement `static/js/contact.js` using `event.preventDefault()`.
  - Validate that required fields are not empty or solely whitespace using `.trim()`.
  - Safely encode subject and body with `encodeURIComponent` to protect special characters (`&`, `?`, `#`, newlines).
  - Pass the recipient address directly through `data-address` from page front matter (`contact_address: "you@example.org"`).
  - Trigger the visitor's configured mail client via `window.location.href = href`.
- **Honest Communication & Fallbacks**:
  - State clearly in `content/contact/index.md` that nothing is sent anywhere until the visitor sends the email themselves.
  - Provide a readable, plain-text email address (`you@example.org`) on the page as an alternative for visitors without a registered desktop mail handler.
  - Explain why static sites cannot keep secrets (API keys) and must use build-time fetching or self-hosted proxy functions instead.
- **Navigation & Multilingual Integration**:
  - Extend the footer note in `layouts/_partials/footer.html` with `or <a href="{{ "contact/" | relLangURL }}">send a message</a>.`
  - Conditionally handle the Kurdish footer link so it does not point to a non-existent page until translated.
  - Document the template, script, and privacy working agreement in `AGENTS.md`.

---

## 📁 What Changed in Chapter 17 (Additive from Chapter 16)

```text
my-knowledge-site/
+-- content/
|   +-- contact/
|       +-- index.md                           # [NEW] Contact page content with front matter address & plain text alternative
+-- layouts/
|   +-- contact/
|   |   +-- page.html                          # [NEW] Accessible form layout template with data-address attribute
|   +-- _partials/
|       +-- footer.html                        # [UPDATED] Extended footer note with language-aware Contact link
+-- static/
|   +-- js/
|   |   +-- contact.js                         # [NEW] Client-side validation & mailto handoff script
|   +-- css/
|       +-- site.css                           # [UPDATED] Added contact-form styles and font-family: inherit
+-- AGENTS.md                                  # [UPDATED] Documented Contact template, script, and zero-server agreement
+-- README.md                                  # [UPDATED] Comprehensive guide for Chapter 17
```

---

## 🚀 Running and Testing Locally

### 1. Build and Preview with Hugo
```bash
# Preview the site locally
hugo server

# Open the Contact page at:
# http://localhost:1313/my-knowledge-site/contact/
```

### 2. Verify Output and Build Strictness
```bash
# Build the site and panic immediately on any warning or deprecation
hugo --minify --panicOnWarning
```

### 3. Run Automated Validation Tests
Run all chapter test suites to ensure both additive features and backward compatibility pass:
```bash
# Run Chapter 17 validation suite
python -m unittest tests/test_chapter_17.py -v

# Run the complete test suite (Chapters 01 - 17)
python -m unittest discover tests -v
```

---

## 🔍 Key Architectural Lessons

### 1. The Three Places Work Can Happen
| Where | When it runs | Capabilities & Trade-offs |
| --- | --- | --- |
| **Build time** | Once, during `hugo` generation | Fastest, completely static, zero runtime dependencies, impossible to crash in front of users. |
| **Visitor's browser** | Every time the page loads | Dynamic, interactive, responsive to inputs; restricted to the data already present on the page; client-dependent. |
| **External server** | When invoked via network request | Can store data, send emails, charge cards; introduces maintenance, operational costs, security risks, and privacy duties (GDPR, cookie notices). |

### 2. Why Secrets Cannot Exist on a Static Site
Any file delivered to the browser (HTML, CSS, JS, JSON) is fully readable by anyone opening Developer Tools. An API key placed in client-side code is a publicly published secret. When interacting with APIs requiring credentials:
- Fetch data **at build time** using Hugo functions (`resources.GetRemote`) with keys stored as CI secrets.
- Or route requests through a **backend proxy/serverless function** that you maintain.
