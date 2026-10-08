# Security policy

## Reporting a vulnerability

Please report security issues privately through
[GitHub private vulnerability reporting](https://github.com/metergraph/skills/security/advisories/new)
(the repository's **Security** tab, "Report a vulnerability"). Do not open a public issue, and do not
include real credentials, tokens or customer data in a report.

## What these skills can do

The skills are instructions, not code. They run with whatever tools the agent already
has. They are written to keep these boundaries:

- **No credentials in chat.** They never ask for, print or store a key. Keys go in the
  client's private settings or the project's `.env`, which `metergraph setup` writes.
- **Approval before spending or sending data.** Starting an analysis or a replay sends
  copies of captured prompts to other model providers and costs money. The skills stop
  and ask first, and state which workload, which models, how many traces and the
  expected cost.
- **No hidden settings changes.** Replay opt-out, data residency, candidate models and
  route limits are changed by a person in the Metergraph app. The skills link to the
  page and explain the change; they do not click through it on the person's behalf
  unless asked to for that specific change.
