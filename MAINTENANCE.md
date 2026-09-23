# Maintenance routine

## Every few months
- Read each page body for claims that are no longer true.
- Compare each translation's source_checked date with its English source.
- Check that every published address still resolves.
- Review open questions in MAINTENANCE.md and AGENTS.md.

## When a dependency changes
- Read the release notes.
- Update HUGO_VERSION in both workflow files on a branch.
- Build locally, then let the checks build the proposal.
- Update action versions one at a time.

## After any mistake reaches the live site
- Use git revert, not git reset, on published history.
- Verify the live result, not only the build.

## Decisions to keep
- The contact form sends nothing to any server.
- Project status values are planned, in-progress, complete, or archived.
- Addresses that have been published get an alias if they must move.

## Next review
- Scheduled date: 2026-12-01
