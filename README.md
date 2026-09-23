# SSG Playground — Chapter 15: Help Readers Find and Use Your Content

Welcome to the hands-on playground repository for **Chapter 15** of *Static Site Generators in the Age of AI*.

This branch (`chapter-15`) is **additive from `chapter-14`**. It focuses on discoverability and reader experience: establishing distinct document titles and metadata descriptions, enabling RSS feed autodiscovery, inspecting generated XML sitemaps, and building a lightweight, progressively-enhanced client-side search page generated directly from your content.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

## 🎯 Chapter 15 Goals

- **Distinct Document Titles and Metadata Descriptions**:
  - Distinguish the home page title (`My Knowledge Notebook`) from subpages (`Title | My Knowledge Notebook`) using `{{ if .IsHome }}`.
  - Define a site-wide fallback description in `hugo.toml` under `[params]`.
  - Output a `<meta name="description">` tag using `{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}`.
  - Provide a `<link rel="canonical" href="{{ .Permalink }}">` tag.
- **XML Sitemaps and RSS Feed Discovery**:
  - Understand `/sitemap.xml` for search engine indexing and `/index.xml` for subscriber feed readers.
  - Add feed autodiscovery in `<head>` using `{{ with .OutputFormats.Get "rss" }}`.
  - Use `$` (`$.Site.Title`) to escape inner template contexts and access top-level page data.
- **Progressively-Enhanced Content Search**:
  - Generate the searchable page list in HTML at build time using `.Site.RegularPages`.
  - Filter out the Search page itself using `{{ if ne .RelPermalink $.RelPermalink }}`.
  - If JavaScript is disabled, the page remains completely functional as a complete, accessible directory of all site content.
  - Implement client-side filtering via `static/js/search.js` with case-insensitive substring matching.
  - Update a live announcement paragraph (`role="status"`) as queries are typed.
  - Use `.search-item[hidden] { display: none; }` to ensure filtered elements do not receive keyboard focus.
- **Navigation Integration**:
  - Add Search to the main `<nav>` menu in `layouts/baseof.html`.
  - Check responsiveness at mobile widths to confirm smooth flex wrapping.
- **Diagnose Silent Failures**:
  - Test the "designed failure": changing the list ID from `search-index` to `search-list` produces no console error because guard clauses return quietly.
  - Diagnose the issue through observable symptoms: an empty status paragraph indicates the script exited early.
- **Reader-Centric vs. Automated Audits**:
  - Test keyboard navigation (Tab through skip link, nav, search input, and only visible results).
  - Test with JavaScript disabled to verify fallback usability.
  - Understand that automated audits (e.g., Lighthouse, axe) verify mechanical rules (alt text, contrast, meta tags) but cannot evaluate content truth, source validity, or result relevance.
- **Enrich Content Descriptions**:
  - Add accurate front matter descriptions to `content/about/index.md` and `content/resources/index.md`.
  - Update `AGENTS.md` to document the new search template and JavaScript paths.

---

## 📁 What Changed in Chapter 15 (Additive from Chapter 14)

```text
my-knowledge-site/
├── hugo.toml                                  # [UPDATED] Added [params] description fallback
├── layouts/
│   ├── baseof.html                            # [UPDATED] Head metadata (title, description, canonical, RSS) & search nav
│   └── search/
│       └── page.html                          # [NEW] Search page template generating build-time index
├── content/
│   ├── search/
│   │   └── index.md                           # [NEW] Search content page
│   ├── about/
│   │   └── index.md                           # [UPDATED] Added front matter description
│   └── resources/
│       └── index.md                           # [UPDATED] Added front matter description
├── static/
│   ├── js/
│   │   └── search.js                          # [NEW] Progressive client-side search script
│   └── css/
│       └── site.css                           # [UPDATED] Search form styles and hidden element display rule
├── AGENTS.md                                  # [UPDATED] Added search template and script under Files
├── .github/workflows/                         # [From Chapter 7 & 14] Deployment and CI checks
└── tests/
    ├── test_chapter_01.py ... test_chapter_14.py
    └── test_chapter_15.py                     # [NEW] Automated tests for titles, metadata, search markup & script
```

---

## 🔍 Search Layout & Progressive Script

### Template (`layouts/search/page.html`)

```html
{{ define "main" }}
  <article>
    <h1>{{ .Title }}</h1>
    {{ partial "page-meta.html" . }}
    {{ .Content }}

    <form class="search-form" role="search">
      <label for="search-query">Search titles and descriptions</label>
      <input type="search" id="search-query" name="q" autocomplete="off">
    </form>

    <p id="search-status" role="status"></p>

    <ul id="search-index">
      {{ range .Site.RegularPages }}
        {{ if ne .RelPermalink $.RelPermalink }}
          <li class="search-item">
            <a href="{{ .RelPermalink }}">{{ .Title }}</a>
            {{ with .Description }}
              <p>{{ . }}</p>
            {{ end }}
          </li>
        {{ end }}
      {{ end }}
    </ul>

    <script src="{{ "js/search.js" | relURL }}" defer></script>
  </article>
{{ end }}
```

### Script (`static/js/search.js`)

```javascript
(function () {
  var form = document.querySelector(".search-form");
  var input = document.getElementById("search-query");
  var list = document.getElementById("search-index");
  var status = document.getElementById("search-status");

  if (!form || !input || !list || !status) {
    return;
  }

  var items = list.querySelectorAll(".search-item");

  function filter() {
    var query = input.value.trim().toLowerCase();
    var shown = 0;

    items.forEach(function (item) {
      var match = query === "" || item.textContent.toLowerCase().includes(query);
      item.hidden = !match;
      if (match) {
        shown += 1;
      }
    });

    if (query === "") {
      status.textContent = "Showing all " + items.length + " pages.";
    } else if (shown === 0) {
      status.textContent = "No pages match that word.";
    } else {
      status.textContent = shown + " of " + items.length + " pages match.";
    }
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  input.addEventListener("input", filter);
  filter();
})();
```

---

## 🧪 Testing & Verification

Run the automated test suite across all chapters:

```bash
# Run unit tests across all chapters (Chapters 01 through 15)
python -m unittest discover tests

# Build site with strict checks
hugo --minify --panicOnWarning

# Local preview server
hugo server
```

All 95 test assertions should pass cleanly.
