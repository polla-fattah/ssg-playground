# SSG Playground — Chapter 08: Work with an AI Agent on Your Hugo Site

Welcome to the hands-on playground repository for **Chapter 8** of *Static Site Generators in the Age of AI*.

This branch (`chapter-08`) is **additive from `chapter-07`**. It introduces the professional methodology for collaborating safely with an **AI coding agent** on your Hugo website—defining project boundaries via `AGENTS.md`, crafting bounded tasks, inspecting changes independently, and maintaining human control over commits and deployments.

---

## 🎯 Chapter 8 Goal

Establish a disciplined, repeatable human-in-the-loop agent workflow:
- Configure persistent project guidance and safety guardrails in `AGENTS.md`.
- Distinguish between **Inspection (Read-Only)** and **Execution (Workspace-Write)** modes.
- Provide bounded prompts with observable constraints (specific target files, exact section placements, word limits, preserved front matter).
- Perform independent code and rendered review using `git diff` and local Hugo preview rather than relying solely on the agent's summary.
- Add the **"How to use these resources"** guidance section to `content/resources/index.md`.
- Catch link and path mistakes that pass `hugo build` but fail at runtime (e.g. relative vs absolute URLs on project sites).

---

## 📁 What Changed in Chapter 8 (Additive from Chapter 7)

```text
my-knowledge-site/
├── AGENTS.md                                  # [NEW] Persistent project guidance & safety agreements
├── content/
│   └── resources/
│       └── index.md                           # [UPDATED] Added "How to use these resources" section
├── layouts/
├── static/
├── .github/
│   └── workflows/
│       └── hugo.yaml
├── hugo.toml
└── tests/
    └── test_chapter_08.py                     # [NEW] Automated validation tests for Chapter 8
```

---

## 📜 The `AGENTS.md` Specification

`AGENTS.md` is an open standard file located at the repository root that AI agents read at the beginning of each session:

```markdown
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
```

---

## ✍️ Content Update: `content/resources/index.md`

The agent successfully authored the following bounded section (under 70 words, exactly 3 bullets, reusing existing destinations):

```markdown
## How to use these resources

- Consult the [Hugo documentation](https://gohugo.io/documentation/) when you need details about configuration, content, or templates.
- Read [my first learning note](../articles/first-learning-note/) for a practical editing and checking example.
- Visit [my knowledge notebook project](../projects/learning-notebook/) to understand this website's purpose.
```

---

## 🔍 The 6-Step Agent Review Method

1. **Clean Baseline**: Ensure `git status` is clean before invoking an agent.
2. **Context & Boundaries**: Point the agent to `AGENTS.md` and define the exact target file.
3. **Bounded Task**: Specify exact headings, bullet counts, word limits, and files to leave untouched.
4. **Git Inspection**: Run `git diff` and `git status` in your own terminal to verify every modified line.
5. **Runtime Verification**: Run `hugo server` and click the links yourself. (Remember: `hugo build` can pass even when an internal link omits the project subfolder!).
6. **Human Staging & Commit**: You decide whether to accept the work and record the commit.

---

## 🧪 Automated Testing

Automated tests for Chapters 1 through 8 are in the `tests/` directory:

```bash
# Run all chapter tests
python -m unittest discover tests

# Or run Chapter 8 tests specifically
python tests/test_chapter_08.py
```

### What `test_chapter_08.py` Verifies:
1. **Build Success**: Validates `hugo --minify --panicOnWarning` compiles cleanly.
2. **`AGENTS.md` Presence & Rules**: Ensures the project guidance file exists with essential safety guardrails.
3. **No Unintended Pages**: Confirms `AGENTS.md` is not accidentally rendered as a public web page.
4. **Resources Section Criteria**:
   - Section heading `## How to use these resources` exists.
   - Contains exactly 3 bullet points.
   - Strict word limit (under 70 words).
   - Valid relative internal links (`../articles/first-learning-note/` and `../projects/learning-notebook/`).
   - Original sections (`Website publishing` and `Examples from this notebook`) preserved.
5. **Rendered HTML Output**: Verifies the compiled page renders all links correctly.

---

## ⏩ Next Step: Chapter 9

In **Chapter 9: Give Your Hugo Content a Consistent Structure**, you will learn how to standardize your content using Archetypes, structured Front Matter, and Hugo content taxonomies!
