# Metergraph skills

[![CI](https://github.com/metergraph/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/metergraph/skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Agent skills for [Metergraph](https://www.metergraph.dev/). They teach Claude Code,
Claude Desktop, Codex and Cursor how to set up Metergraph, investigate your LLM traffic
and take a workload through a model-swap analysis, using the tools your Metergraph
connection already provides.

Skills are instructions, not code. They add no tools and no access: everything they do
goes through the Metergraph MCP server you connect, with the key you give it. They stop
and ask before anything that spends money or sends captured prompts to a model provider.

## Skills

| Skill | Use it to |
| --- | --- |
| [`metergraph`](skills/metergraph/SKILL.md) | Set up Metergraph for your client, runtime and deployment, and answer documentation questions |
| [`metergraph-onboarding`](skills/metergraph-onboarding/SKILL.md) | Instrument an application and verify its first real trace |
| [`metergraph-investigate`](skills/metergraph-investigate/SKILL.md) | Explain a failed or unusual trace, a usage question or an incident from workspace evidence |
| [`metergraph-analyze`](skills/metergraph-analyze/SKILL.md) | Take one classified workload to a model-swap recommendation: readiness, confirmation, start, poll and report |

## Install

### Claude Code

```sh
claude plugin marketplace add metergraph/skills
claude plugin install metergraph@metergraph-agents
```

Or, inside Claude Code, `/plugin marketplace add metergraph/skills` and then
`/plugin install metergraph@metergraph-agents`. Skills appear as `/metergraph:<skill>`.

### Claude Desktop

Customize → Plugins → Add marketplace, and enter `metergraph/skills`. To add a single
skill instead, download its zip from the
[latest release](https://github.com/metergraph/skills/releases/latest) and upload it under
Customize → Skills. Skills need code execution turned on.

### Codex, Cursor and other agents

With the Metergraph CLI, in your project:

```sh
npx --yes metergraph-cli@next skill install --client codex --runtime local
```

Or with the [skills](https://github.com/vercel-labs/skills) installer:

```sh
npx skills add metergraph/skills
```

### Connect Metergraph

The skills need a Metergraph MCP connection to do anything beyond setup. Ask your agent
to use the `metergraph` skill, or follow the
[agent access guide](https://www.metergraph.dev/docs/guides/agent-access/).

## Where these skills are used

This repository is the source of truth for every Metergraph skill. The setup skill
published at https://www.metergraph.dev/SKILL.md, the copy bundled in the
[`metergraph-cli`](https://github.com/metergraph/cli) npm package and the
`metergraph-skills` PyPI package are generated from `skills/metergraph/SKILL.md` at a
pinned commit, and their CI fails if they drift.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues privately, as described in
[SECURITY.md](SECURITY.md).

## License

[Apache-2.0](LICENSE)
