# Brief: My Knowledge Notebook

## Audience
Students learning static website publishing and readers interested in structured note-taking with AI assistance. Not prospective web design agency clients, and not the general public seeking a blogging platform.

## Purpose
A reader should be able to find practical learning notes, inspect small ongoing and archived projects, browse selected documentation references, search articles by topic, and optionally send a message via email handoff.

## Success
A student can clone the repository, run `hugo server`, pass all automated CI validation checks locally without errors, and follow the project's evolution across chapters.

## Content
- Exists: 2 learning articles (`first-learning-note`, `publishing-with-github-pages`), 2 project dossiers (`learning-notebook`, `reading-list`), 5 verified resources in JSON, About and Search pages, and Kurdish translations for home and About.
- To write: Additional notes on CI automation and Hugo templating.
- Written by the notebook author; translations verified with native review.

## Out of scope
- Not a dynamic content management system (CMS); no server-side databases or user accounts.
- No third-party analytics trackers, cookies, or remote form endpoints.
- No unreviewed machine translations.
- No secret credentials or API keys stored in client-side code or repository commits.

## Capabilities
| Capability | Status | Justification / Ongoing Cost |
| --- | --- | --- |
| Markdown pages & sections | Yes | Core publishing mechanism; re-read periodically for stale claims. |
| Layout & CSS stylesheet | Yes | Semantic HTML5 structure and clean plain CSS. |
| Git history & recovery | Yes | Transparent version control and auditability via `git revert`. |
| GitHub Pages publishing | Yes | Automated deployment workflow with pinned Hugo version. |
| Agent working agreements | Yes | `AGENTS.md` guidelines kept up-to-date with repository realities. |
| Content model & archetypes | Yes | Standardized metadata and section structures. |
| Templates & partials | Yes | Reusable layout components (`page-meta`, `resource-directory`, etc.). |
| JSON data directory | Yes | Structured `resource_links.json` validated in templates and CI. |
| Checks on every proposal | Yes | Automated PR checks enforcing relative links, booleans, and versions. |
| Titles, descriptions, sitemap, feed | Yes | Essential discoverability and reader accessibility. |
| Site search | Yes | Progressive enhancement with build-time index and client-side filtering. |
| Second language (Kurdish Sorani) | Yes | Multilingual support with `locale`, `direction`, and `i18n` parity. |
| Contact form (mail handoff) | Yes | Privacy-respecting client-side form validating input without servers. |
| Maintenance routine | Yes | Written routine in `MAINTENANCE.md` with scheduled audit questions. |

## Review and Maintenance
- **Author & Maintainer:** Polla Fattah
- **Reviewer:** Native language reviewer for Kurdish strings; peer review on pull requests.
- **Routine:** Maintenance pass every few months as specified in `MAINTENANCE.md`.
- **Merge Policy:** All checks in `.github/workflows/checks.yaml` must pass cleanly before merging.
- **Next Review Date:** 2026-12-01
