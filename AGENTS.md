# Project guidance

This is a small Hugo knowledge website using Markdown and plain CSS.

## Files

- Content lives in content/.
- Source material for content work is in sources/.
- Articles are page bundles under content/articles/, each with its own index.md.
- The Articles landing page and its manual list are in content/articles/_index.md.
- The home page and its Latest writing list are in content/_index.md.
- Shared HTML structure is in layouts/baseof.html.
- General page content is in layouts/all.html.
- The Projects landing-page template is layouts/projects/section.html.
- Reusable components are in layouts/_partials/.
- Resource-directory records are in assets/data/resource_links.json.
- The Resources page template is layouts/resources/page.html.
- Resource-directory rendering is in layouts/_partials/resource-directory.html.
- The Search page template is layouts/search/page.html.
- The search script is static/js/search.js.
- The Contact page template is layouts/contact/page.html.
- The contact script is static/js/contact.js.
- Interface strings are in i18n/en.toml and i18n/ckb.toml.
- Kurdish pages are the .ckb.md files beside their English versions.
- The language switcher is layouts/_partials/language-links.html.
- The stylesheet is static/css/site.css.
- Site configuration is hugo.toml.
- The publishing workflow is .github/workflows/hugo.yaml.
- The maintenance routine is in MAINTENANCE.md.

## Working agreements

- Read the relevant source before proposing or making a change.
- Change only the source files requested for the current task.
- Preserve existing front matter, URLs, and authored facts unless the task asks otherwise.
- For content tasks, use only the source files named in the task. Do not search the web or add material from memory.
- Do not state anything the named source does not support. Where the source records a gap, say that it is unknown rather than estimating.
- Credit every external reference in a Sources section in the page body, with a link and a short explanation.
- New articles use title, description, and draft in front matter, and the headings What this is about, What happened, What I would do differently, and Sources.
- Leave new pages at draft: true. Publication is the reader's decision.
- Resource records use title, url, description, topics (an array of strings), and start_here (a Boolean). Preserve these types and do not invent descriptions or destinations.
- Never change a translated page's meaning to match a template. Translations keep English front-matter field names and translate only their values.
- Do not invent experiences, qualifications, sources, or claims about the author.
- Use the installed Hugo; do not add dependencies or change the publishing workflow unless requested.
- Do not edit generated public/ or resources/ files by hand.
- When asked to check a change, run hugo --minify --panicOnWarning and report the result accurately.
- If a check cannot run, explain what prevented it and what remains unchecked.
- The contact form prepares a message in the visitor's own mail client and sends nothing to any server. Do not replace it with a form service, an analytics script, or any request to a third party without being asked.
- Archiving a page means changing its status and saying so in the body. It does not mean setting draft: true, which withdraws a published address.
- Leave staging, committing, pushing, and deployment to the reader unless explicitly delegated.
