# Metergraph

[Privacy Policy](https://www.metergraph.dev/privacy) ·
[Support](https://github.com/metergraph/skills/issues) ·
[Documentation](https://www.metergraph.dev/docs/) ·
[Terms of Service](https://www.metergraph.dev/terms)

Twelve skills to check model list prices, connect Metergraph, investigate LLM
usage, and evaluate model changes against authorized workspace evidence.

## Get started

Price checking needs no account. Workspace workflows need a separately authorized
Metergraph CLI or MCP connection. This plugin supplies instructions, not a bundled
MCP server, hooks, background service or executable. It uses tools already available
in the client; some setup workflows require a local shell and Docker. If a client
cannot perform a step, the skill explains the limitation and hands it to the user.

Try these prompts:

- "Check this repository's models against public prices. Do not change the code."
- "Show my Metergraph workspace's busiest routes for the last seven days."
- "Help me plan a cheaper-model evaluation for one workload. Ask before running it."

## Data handling and external services

- **Repository inspection:** price-check reads relevant source and sanitized example
  configuration. It excludes secret files. Only model identifiers and provider/channel
  names are sent to `https://app.metergraph.dev/v1/pricing/`; no account is required.
- **Workspace operations:** authorized CLI/MCP calls go to the user's selected
  Metergraph deployment (hosted at `https://app.metergraph.dev`, or a customer-operated
  deployment). Reads can return usage metadata and, where scoped and authorized,
  retained trace content. Trace content may contain personal data supplied by the
  customer's application. Setup can configure application telemetry; imports and
  evaluation workflows can create retained workspace records.
- **Model evaluations and replay:** separately approved runs can send selected
  captured prompts to the model providers configured for that workspace. The user
  chooses models, scope and budget before execution. Provider retention and privacy
  terms also apply; review those for the selected provider before authorizing a run.
- **Public guides and releases:** setup may access https://www.metergraph.dev and
  public GitHub releases. Customer-local installation requires the signed bundle's
  documented verification and supported transport. Installation and execution are
  explicit setup actions, not background behavior on plugin installation.

The plugin has no independent storage service. Metergraph's hosted service retains
workspace data according to its [retention and deletion notice](https://www.metergraph.dev/retention):
free workspace traces are queryable for 90 days; managed retention depends on the
customer agreement. Customer-operated deployments and model providers have their
own retention settings. Reports can also be saved locally when the user requests it.
Never put credentials or raw trace content in support reports.

See [Privacy Policy](https://www.metergraph.dev/privacy), the applicable
[PSL privacy policy](https://www.psl.com/legal), and
[Terms of Service](https://www.metergraph.dev/terms). For data access or deletion,
contact studio-legal@psl.com.

## Help and troubleshooting

If the connection is missing or access is denied, reconnect to the intended workspace
using the client's supported private authentication settings. Never provide secrets
in chat. Missing provider, content or transport capabilities are explicit blockers;
a successful connection alone does not prove a completed analysis.

- [Documentation](https://www.metergraph.dev/docs/)
- [Setup guide](https://www.metergraph.dev/docs/start/first-trace/)
- [Support](https://github.com/metergraph/skills/issues)
- [Private security reports](https://github.com/metergraph/skills/security/advisories/new)

Source: [metergraph/skills](https://github.com/metergraph/skills). Apache-2.0 license.
