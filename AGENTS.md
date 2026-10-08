# Public repository contribution rules

This repository is public. Before publishing a branch, commit, issue, pull
request, comment, release, screenshot, fixture, or log:

- Write a self-contained public description. Keep private tracker IDs, links,
  discussion, and customer context in the internal tracker. Do not put them in
  public branch names, commit messages, issue or PR text, or release notes.
- Remove secrets, tokens, non-public customer or prospect names and domains,
  tenant or workspace IDs, captured prompts or responses, private paths, and
  cloud account or resource IDs. Use synthetic examples and `example.com`.
- Inspect the exact diff and metadata before pushing or posting. Run
  `python3 scripts/check_publication.py origin/main` before pushing. CI repeats
  the check, but a CI failure cannot undo a public disclosure.
- Report security issues through this repository's private vulnerability
  reporting path, not a public issue.

If unsure whether a detail is public, stop and ask before publishing.

# Writing skills

- One skill per directory under `skills/`, named `metergraph-<stage>`. The
  directory name must equal the `name` in the frontmatter.
- Name only tools that the public Agent Access guide documents, or that
  `metergraph_get_capabilities` reports. When a step has no tool, say so and
  hand the person the app page instead of inventing one.
- Every step that spends money, replays traffic to a provider or changes
  workspace settings must stop for the person's explicit approval.
- Run `node scripts/validate.mjs` before pushing.
