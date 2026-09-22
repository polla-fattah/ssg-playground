# Project guidance

This is a small Hugo knowledge website using Markdown and plain CSS.

## Files

- Content lives in content/.
- The shared layout is layouts/all.html.
- The stylesheet is static/css/site.css.
- Site configuration is hugo.toml.
- The publishing workflow is .github/workflows/hugo.yaml.

## Working agreements

- Read the relevant source before proposing or making a change.
- Change only the source files requested for the current task.
- Preserve existing front matter, URLs, and authored facts unless the task asks otherwise.
- Do not invent experiences, qualifications, sources, or claims about the author.
- Use the installed Hugo; do not add dependencies or change the publishing workflow unless requested.
- Do not edit generated public/ or resources/ files by hand.
- When asked to check a change, run hugo --minify --panicOnWarning and report the result accurately.
- If a check cannot run, explain what prevented it and what remains unchecked.
- Leave staging, committing, pushing, and deployment to the reader unless explicitly delegated.
