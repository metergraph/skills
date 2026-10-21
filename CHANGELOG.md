# Changelog

## Unreleased

- Work through the `metergraph` CLI or the Agent Access MCP server, whichever the agent has. The model-swap loop skills share one discovery step that uses the CLI's `tools` commands when the installed CLI has them and MCP otherwise, and each tool is called the same way on both paths. From the CLI, a call that writes, starts work or calls a provider takes `--yes` only after the person approves that exact call. The skills no longer report a missing MCP server when the CLI works, or the reverse, and setup and investigation fall back to the other path instead of stopping.
- Name access by the job it does. Read access is the Metadata role; loop access is the Debug role plus evaluation writes, evaluation previews and analysis starts. The loop checks loop access once before it starts and says how to get it on each deployment: `metergraph login --access loop` or the Keys page on the hosted service, `bin/agent-key` on the customer-local bundle, and not offered on customer-owned AWS or the open-source server.
- Correct the access needed to start an analysis: the Debug role plus Allow analysis starts.
- Refer to workspaces by slug, never by ID, in commands, examples and confirmations.
- Make the CLI the default setup path for agents with a shell, and describe MCP for clients without one or when the person prefers it.

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
