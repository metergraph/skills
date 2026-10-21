# Changelog

## 0.7.0

- On the customer-local bundle, give a coding agent analysis access with `bin/agent-key` when the bundle has it. The agent explains each grant and the person chooses which to give; the key goes to a private file the agent never opens or prints. Bundles without the command keep the Keys page route, and the agent never uses the local admin login.

## 0.6.0

- Add the local-bundle skill for verifying and starting the signed customer-local bundle.
- Guide setup according to where the agent runs, including Metadata-key reads for remote agents and the open-source server's static-token route.
- Prefer the installed CLI for bounded investigation reads, with capability checks and MCP fallback.
- Answer cost questions using grouped usage and exact metadata filters, with explicit coverage, missing-value and attribution limits.
- Require comparable observed usage before describing a code change's cost impact.
- Show returned analysis stages and report availability without inventing progress or completion estimates.
- Use the latest stable CLI fallback and keep workspace identity out of public repositories and CI logs.
- Keep non-hosted setup and unpinned CLI sessions on the appropriate supported path.
- Match investigation windows, bounds and trace fields to the CLI contract, including rolling legacy windows and filtered trace reads.
- Preserve successful anomalies and distinguish route latency from per-call latency.

## 0.5.0

Previous tagged release. See the GitHub release notes for its changes.
