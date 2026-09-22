# Raw notes: publishing the notebook

Not for publication as written. Working notes from Chapters 6 and 7.

Reference consulted: GitHub's documentation on configuring a publishing source,
https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

- A Pages site has to be told where its content comes from. We chose the
  GitHub Actions route rather than publishing from a branch.
- The supplied workflow builds with Hugo and deploys the built output.
  We never committed the public/ folder.
- baseURL had to include the repository path. Before that, the live site
  loaded without its stylesheet and the internal links went to the wrong place.
- The first deployment failed. Cause: I pushed before setting the Pages
  source. Fixed by setting it, then running the workflow again.
- The Actions log was where the failure was legible. The browser only
  showed a missing or stale page.
- hugo --minify --panicOnWarning passed locally before that push. Passing
  locally did not mean the deployment had worked.
- Not measured: how long a deployment usually takes.
- Not attempted: a custom domain.
