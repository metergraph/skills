# Metergraph Agent Skills

[![skills.sh](https://skills.sh/b/metergraph/skills)](https://skills.sh/metergraph/skills)
[![CI](https://github.com/metergraph/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/metergraph/skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Agent Skills for [Metergraph](https://www.metergraph.dev/), which learns from your
application's LLM traces, benchmarks models against your real usage and routes each task
to the model that clears your quality bar. These skills let Claude Code, Claude Desktop,
Codex, Cursor and other coding agents set Metergraph up, investigate your LLM traffic and
take a workload through a model-swap analysis.

The skills follow the [Agent Skills](https://agentskills.io/) format. They are
instructions, not code: they add no tools and no access, and everything they do goes
through the Metergraph connection and key you give your agent.

## Transport and provider consent compatibility

The customer-local workflow requires a signed bundle and a released client that
support authenticated Docker transport. It does not send credentials to host
HTTP or use local browser sign-in/consent. Older local setup instructions must
stop at that compatibility boundary; a healthy listener or issued key is not
proof. Hosted authenticated HTTPS remains a separate deployment route.

Provider-backed actions also require trusted human execution consent, separate
from scopes, chat approval and CLI confirmation. Deployments returning
`provider_consent_unavailable` pause agent analysis, classification and experiment
starts. Supported replay receipts require human review of the exact frozen plan
and one exact retry with `consent_id`; agents cannot approve receipts. Reads and
deterministic previews remain available when advertised. See the `metergraph`
skill for the complete gate, which takes precedence over historical examples.

## Quick start

```sh
npx skills add metergraph/skills
```

Then ask your agent:

```
Help me connect Metergraph to this agent.
```

Or, with no account at all:

```
Check this repo's models against Metergraph's pricing and flag any I'm overpaying for.
```

The `metergraph` skill asks which deployment you use (hosted, the customer-local bundle,
customer-owned AWS or the open-source server) and walks you through the connection one
step at a time, without asking for keys in chat.

## Install

### Any agent, with skills.sh

```sh
# All skills, for the agents the installer detects
npx skills add metergraph/skills

# One skill
npx skills add metergraph/skills --skill metergraph-analyze

# See what is available without installing
npx skills add metergraph/skills --list
```

### Claude Code

```sh
claude plugin marketplace add metergraph/skills
claude plugin install metergraph@metergraph
```

Or inside Claude Code: `/plugin marketplace add metergraph/skills`, then
`/plugin install metergraph@metergraph`. Plugin skills are namespaced, for
example `/metergraph:metergraph-analyze`. Restart Claude Code after installing.

### Claude Desktop

Open **Customize → Plugins → Add marketplace** and enter `metergraph/skills`, then
install the `metergraph` plugin.

To add one skill instead, download its zip from the
[latest release](https://github.com/metergraph/skills/releases/latest) and upload it
under **Customize → Skills**. Skills need code execution turned on.

### Codex, Claude Code or Cursor, with the Metergraph CLI

The [Metergraph CLI](https://github.com/metergraph/cli) installs the setup skill into a
project as part of `setup`, or on its own with no sign in and no network access:

```sh
npx --yes metergraph-cli@latest skill install --client codex --runtime local
```

Use `--client claude` or `--client cursor` for the other agents. The CLI records what it
installed and never overwrites a skill you edited.

### By hand

Copy a skill's folder into your agent's skills directory: `.claude/skills/` for Claude
Code, `.agents/skills/` for Codex, or `.cursor/skills/` for Cursor.

## Connect Metergraph

Every skill except `metergraph`, `metergraph-price-check` and `metergraph-local-bundle` needs your agent connected
to a workspace, through either the [Metergraph CLI](https://github.com/metergraph/cli) or
the Agent Access MCP server. Both reach the same tools with the same key: agents with a
shell (Claude Code, Codex, Cursor) use the CLI, and clients without one (Claude Desktop,
ChatGPT) use MCP. Use the `metergraph` skill, or follow the
[agent access guide](https://www.metergraph.dev/docs/guides/agent-access/). The
[MCP server guide](https://www.metergraph.dev/docs/guides/mcp-server/) lists the tools,
and which access role each one needs.

Investigating and choosing a workload need the Metadata role. Saving evals and starting
analyses need the Debug role plus Allow evaluation writes, Allow evaluation previews and
Allow analysis starts, which a workspace owner grants. `metergraph-model-swap` checks for
them before it starts and says how to get them on your deployment.

## Available skills

### metergraph

Connect Metergraph to your agent and answer questions about the docs.

**Use when:**

- Setting up Metergraph for the first time, on any deployment
- Connecting Claude Desktop, Claude Code, Codex or Cursor to a workspace
- Asking what Metergraph can do in your edition

### metergraph-price-check

Find the models a repository calls, look up their list prices in Metergraph's free public
[Pricing API](https://www.metergraph.dev/docs/reference/pricing-api/), and flag calls
that look overpriced for what they do. Needs no account or key. It reports leads, not
answers, and ends by offering Metergraph setup so a swap can be tested on real traffic.

**Use when:**

- Asking whether this codebase pays for more model than its tasks need
- Getting list prices and rough per-call costs for the models in a repository
- Taking a first look before setting Metergraph up

### metergraph-local-bundle

Verify and start a signed commercial customer-local bundle with authenticated
Docker transport; stop unsupported clients before handing over to
`metergraph setup` without exposing local credentials or replacing existing data.

**Use when:**

- Installing the customer-local bundle on a person's own machine
- Setup reports that the local bundle prerequisite is incomplete
- Reusing an existing local bundle installation safely

### metergraph-onboarding

Instrument an application and prove that its first real trace arrived.

**Use when:**

- Adding the Metergraph SDK to an existing codebase
- Checking that a specific trace reached the intended workspace
- Moving from an empty workspace to one with real traffic

### metergraph-investigate

Explain a failure or anomaly from workspace evidence, citing the window, IDs and
coverage it used.

**Use when:**

- A trace failed or looks wrong
- Spend, tokens or latency jumped on a route
- An incident fired and you want to know why

### metergraph-analyze

Take one classified workload to a model-swap recommendation: check readiness and sample
size, confirm the cost before anything runs, start the analysis, follow it and explain
the report.

**Use when:**

- Asking whether a workload could run on a cheaper or better model
- Starting a model-swap analysis from your agent
- Reading what a finished analysis recommends

### The model-swap workflow

Six skills take a workload from choice to a rerun. You choose, define and rerun from your
coding agent, and read the report and inspect evidence in the Metergraph app. Start with
`metergraph-model-swap`; it loads the others as the workflow reaches them.

```
choose workload → choose traces and models → define or refine eval → run analysis
      → summary and report link → inspect evidence in the app → refine and rerun ↺
```

| Skill | Stage |
| --- | --- |
| [`metergraph-model-swap`](skills/metergraph-model-swap/SKILL.md) | The whole workflow: where you are, what comes next, and the rules every stage keeps |
| [`metergraph-workloads`](skills/metergraph-workloads/SKILL.md) | Choose a workload: rank by spend with its source, flag spikes and suspect data, check readiness |
| [`metergraph-candidates`](skills/metergraph-candidates/SKILL.md) | Choose traces and models: environment, candidates, residency and the route settings to change |
| [`metergraph-evals`](skills/metergraph-evals/SKILL.md) | Define or refine the eval: checks and a rubric from good traces and your code, tested before use |
| [`metergraph-analyze`](skills/metergraph-analyze/SKILL.md) | Run the analysis: readiness, cost confirmation, start once, follow it |
| [`metergraph-report`](skills/metergraph-report/SKILL.md) | Summarize: the decision, the numbers behind it, the report link and what to inspect in the app |
| [`metergraph-iterate`](skills/metergraph-iterate/SKILL.md) | Refine and rerun: one change, a new approved run, an honest comparison |

## Example prompts

```
Check this repo's LLM calls against Metergraph's pricing and flag cheaper options.
```

```
Use Metergraph to show my workspace context and capabilities.
```

```
Why did spend on the summarize route triple yesterday?
```

```
Plan a model swap for my largest workload.
```

```
I checked the report. The grader is wrong on the two pricing cases. Fix the eval and rerun.
```

```
Explain the latest Metergraph report and whether we should switch.
```

## What the skills will not do

- **Ask for keys in chat.** Keys go in your client's private settings, or in the `.env`
  that `metergraph setup` writes.
- **Spend money or send your data without a yes.** An analysis or a replay sends copies
  of captured prompts to other model providers and costs money. The skills stop first and
  say which workload, which models and roughly what it will cost.
- **Change workspace settings for you.** Replay opt-out, data residency, candidate models
  and cost limits are yours to change in the Metergraph app; the skills explain the change
  and link to the page.
- **Read captured content unless you ask.** They start from metadata and use trace
  content only with your consent and a key that allows it.

## Repository layout

```
skills/<name>/SKILL.md           one folder per skill; the folder name is the skill name
.claude-plugin/marketplace.json  the metergraph marketplace
.claude-plugin/plugin.json       the metergraph plugin, which includes every skill
scripts/validate.mjs             checks every skill against the rules each client enforces
scripts/package.sh               builds the per-skill zips attached to each release
```

This repository is the source for every Metergraph skill. The setup skill at
https://www.metergraph.dev/SKILL.md, the copy bundled in the
[`metergraph-cli`](https://www.npmjs.com/package/metergraph-cli) npm package and the
[`metergraph-skills`](https://pypi.org/project/metergraph-skills/) PyPI package are
copied from `skills/metergraph/SKILL.md` at a pinned commit, and their CI fails if they
drift.

Releases are tagged `vX.Y.Z` to match `.claude-plugin/plugin.json`, and each release
attaches one zip per skill with a `SHA256SUMS` file.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md), and run
`node scripts/validate.mjs` before you push. Report security issues privately, as
described in [SECURITY.md](SECURITY.md).

## License

[Apache-2.0](LICENSE)
