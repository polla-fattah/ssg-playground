---
title: "What I learned publishing with GitHub Pages"
description: "How this notebook reached a public address, and what went wrong the first time."
draft: false
---

## What this is about

This notebook is published from its own repository rather than uploaded by
hand. Setting that up went wrong once, in a way that was easy to misread.

## What happened

A Pages site has to be told where its content comes from. I chose the GitHub
Actions route rather than publishing from a branch, so a workflow builds the
site with Hugo and deploys the built output. The generated `public/` folder is
never committed.

The first deployment failed, because I pushed before setting the publishing
source. Setting it and running the workflow again fixed it. The failure was
only legible in the Actions log; the browser showed a missing page, which told
me nothing about the cause.

One configuration detail mattered more than I expected: `baseURL` has to
include the repository path. Before I corrected it, the live site loaded
without its stylesheet and its internal links went to the wrong place.

I also learned to distrust a passing local build as evidence about the live
site. `hugo --minify --panicOnWarning` succeeded before the push that failed
to deploy.

## What I would do differently

I would set the publishing source before the first push, and read the Actions
log before looking at the site in a browser.

I have not measured how long a deployment usually takes, and I have not tried
a custom domain, so I cannot say anything useful about either.

## Sources

- [GitHub: configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site): Explains how a Pages site is told where to publish from, including the GitHub Actions route used here.
