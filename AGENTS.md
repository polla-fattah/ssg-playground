# Project guidance

This is a small Hugo knowledge website using Markdown and plain CSS.

## Files

- Content lives in content/.
- Shared HTML structure is in layouts/baseof.html.
- General page content is in layouts/all.html.
- The Projects landing-page template is layouts/projects/section.html.
- Reusable components are in layouts/_partials/.
- Resource-directory records are in assets/data/resource_links.json.
- The Resources page template is layouts/resources/page.html.
- Resource-directory rendering is in layouts/_partials/resource-directory.html.
- The stylesheet is static/css/site.css.
- Site configuration is hugo.toml.
- The publishing workflow is .github/workflows/hugo.yaml.

## Working agreements

- Read the relevant source before proposing or making a change.
- Change only the source files requested for the current task.
- Preserve existing front matter, URLs, and authored facts unless the task asks otherwise.
- Resource records use title, url, description, topics (an array of strings), and start_here (a Boolean). Preserve these types and do not invent descriptions or destinations.
- Do not invent experiences, qualifications, sources, or claims about the author.
- Use the installed Hugo; do not add dependencies or change the publishing workflow unless requested.
- Do not edit generated public/ or resources/ files by hand.
- When asked to check a change, run hugo --minify --panicOnWarning and report the result accurately.
- If a check cannot run, explain what prevented it and what remains unchecked.
- Leave staging, committing, pushing, and deployment to the reader unless explicitly delegated.
