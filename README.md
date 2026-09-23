# SSG Playground - Chapter 12: Build a Resource Directory with JSON

Welcome to the hands-on playground repository for **Chapter 12** of *Static Site Generators in the Age of AI*.

This branch (`chapter-12`) is **additive from `chapter-11`**. It demonstrates how to manage structured, repeatable content using **local JSON data** and Hugo's resource-processing pipeline (`resources.Get` and `transform.Unmarshal`), separating data authoring from template presentation.

## Part of the Open-Source Book

This playground is part of the open-source book **Static Site Generators in the Age of AI**. The original book is available at [polla-fattah/ssg-book](https://github.com/polla-fattah/ssg-book).

---

##  Chapter 12 Goals

- **Structured Data in JSON**: Move repeated resource records into an external JSON asset (`assets/data/resource_links.json`).
- **The 5-Field Resource Model**: Adhere to an explicit editorial schema:
  - `title` (String): Resource name.
  - `url` (String): Full external HTTPS destination.
  - `description` (String): Factual summary sentence.
  - `topics` (Array of Strings): Topic tags.
  - `start_here` (Boolean): Editorial starting-point flag.
- **Hugo Asset Processing**: Fetch and parse data files at build time using `resources.Get` and `transform.Unmarshal`.
- **Collection Delimiting**: Format arrays into readable inline text using `delimit . ", "`.
- **Separation of Concerns**:
  - `content/resources/index.md`: Editorial introduction and internal notebook links.
  - `assets/data/resource_links.json`: Repeated data records.
  - `layouts/_partials/resource-directory.html`: Rendering and HTML presentation.
  - `layouts/resources/page.html`: Page-specific layout for Resources.
- **Data-Driven Ordering**: Reorder, add, or edit resources directly in JSON without modifying templates.
- **Maintain Accurate Agent Guidance**: Update `AGENTS.md` with the new file paths and data-schema working agreements.
- **Format Recognition**: Compare Markdown, JSON, YAML, TOML, CSV, and XML to understand when each format is appropriate.

---

##  What Changed in Chapter 12 (Additive from Chapter 11)

```text
my-knowledge-site/
+-- assets/
|   +-- data/
|       +-- resource_links.json                # [NEW] JSON data file with 3 curated resource records
+-- layouts/
|   +-- resources/
|   |   +-- page.html                          # [NEW] Dedicated layout for content/resources/index.md
|   +-- _partials/
|       +-- resource-directory.html            # [NEW] Partial to fetch, unmarshal, and render resource data
+-- content/
|   +-- resources/
|       +-- index.md                           # [UPDATED] Removed manual "Website publishing" markdown list
+-- AGENTS.md                                  # [UPDATED] Added JSON file paths and data typing agreement
+-- layouts/
|   +-- baseof.html                            # [From Chapter 11] Shared document frame
|   +-- all.html                               # [From Chapter 11] General content layout
|   +-- projects/section.html                  # [From Chapter 11] Projects section layout
+-- static/                                    # [From Chapter 5] CSS styling
+-- tests/
    +-- test_chapter_01.py ... test_chapter_11.py
    +-- test_chapter_12.py                     # [NEW] Automated tests for JSON data and rendered directory
```

---

##  The 5-Field Resource Data Model

Located at `assets/data/resource_links.json`:

```json
[
  {
    "title": "Hugo documentation",
    "url": "https://gohugo.io/documentation/",
    "description": "The official reference for Hugo configuration, content, and templates.",
    "topics": ["Hugo", "Reference"],
    "start_here": true
  },
  {
    "title": "Hugo template introduction",
    "url": "https://gohugo.io/templates/introduction/",
    "description": "An introduction to template expressions, functions, and context in Hugo.",
    "topics": ["Hugo", "Templates"],
    "start_here": false
  },
  {
    "title": "Hugo page bundles",
    "url": "https://gohugo.io/content-management/page-bundles/",
    "description": "An explanation of grouping a page with related resources.",
    "topics": ["Hugo", "Content organisation"],
    "start_here": false
  }
]
```

---

##  Template Implementation (`layouts/_partials/resource-directory.html`)

```html
<h2 id="website-publishing">Website publishing</h2>
{{ with resources.Get "data/resource_links.json" }}
  <ul>
    {{ range . | transform.Unmarshal }}
      <li>
        <a href="{{ .url }}">{{ .title }}</a>
        {{ if .start_here }}
          <strong>Start here</strong>
        {{ end }}
        <p>{{ .description }}</p>
        {{ with .topics }}
          <p><strong>Topics:</strong> {{ delimit . ", " }}</p>
        {{ end }}
      </li>
    {{ else }}
      <li>No resources to display yet.</li>
    {{ end }}
  </ul>
{{ else }}
  {{ errorf "Missing resource directory data: assets/data/resource_links.json" }}
{{ end }}
```

---

##  Automated Testing

Run the automated test suite across all chapters:

```bash
# Run Chapter 12 specific tests:
python -m unittest tests/test_chapter_12.py

# Run all tests across Chapters 1 through 12:
python -m unittest discover tests
```

### Test Coverage in `test_chapter_12.py`:
1. `test_hugo_build_clean`: Verifies clean Hugo build with zero warnings or errors.
2. `test_resource_links_json_model`: Validates valid JSON syntax, 3 records, expected key types, Boolean `start_here`, and agreed ordering.
3. `test_templates_exist`: Confirms `layouts/resources/page.html` and `layouts/_partials/resource-directory.html` exist.
4. `test_rendered_resources_page_content`: Verifies generated HTML includes all 3 records, `#website-publishing` heading, "Start here" badge on record 1, comma-delimited topics, and preserved markdown prose.
5. `test_agents_md_updated_with_json_spec`: Ensures `AGENTS.md` documents data file locations and type agreements.

---

##  Git Checkpoint

Commit the completed chapter changes:
```bash
git add assets/data/resource_links.json layouts/resources/page.html layouts/_partials/resource-directory.html content/resources/index.md AGENTS.md tests/ README.md
git commit -m "Build the Resources directory from local JSON records"
```
