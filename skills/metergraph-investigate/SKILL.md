---
name: metergraph-investigate
description: Investigate a failed or anomalous LLM trace, usage spike, cost question (which route, provider or model costs most, a daily trend, a change from the prior period), incident or whether a code change moved cost through an already connected Metergraph Agent Access server, answering only from bounded, cited evidence. Use after setup is verified; use the metergraph skill first when not connected.
---

# Investigate with Metergraph evidence

This skill expands the bounded investigation section of the public `metergraph`
skill. It adds no tools, scopes or authority. When no Metergraph MCP server is
connected, or the user has not chosen a client, runtime and deployment, stop and
use the `metergraph` skill for setup routing. Never ask for, echo or store a
key.

## 1. Discover before reading data

1. Call `metergraph_get_workspace_context`, then `metergraph_get_capabilities`.
   Do not call any other Metergraph tool first.
2. Confirm with the user that `provenance.workspace_id`, the workspace name and
   `provenance.deployment_profile` match the installation they intend. A staging
   or demo workspace is not their production workspace. Stop on a mismatch,
   an authorization error, or revoked or expired access, and tell the human to
   reconnect through their client's secure flow.
3. Build the tool plan only from what the server returns: the workspace
   context's `access.scopes`, and each capability under the capabilities
   response's `agent` object with its `available`, `privacy_class` (metadata,
   content or replay), `required_scope`, `mutates` and `external_calls`, plus
   `bounds` (`max_days`, `max_rows`). Treat the tools your client lists as the
   only callable tools. A tool or capability that is absent, or has
   `available: false`, is a blocker to report, not something to
   guess, retry under another name or replace with a dashboard API, generic SQL
   or a shell command. Some deployments are content-blind or have no replay,
   incidents, ingestion health or reports.

## 2. Fix the question and the bound

Restate the question, the route or workload if known, and an explicit UTC
window. Windows are UTC: `days: N` means the current UTC day so far plus the
`N - 1` whole UTC days before it, so today is always partial; `since`
(inclusive) and `until` (exclusive) give an exact window of at most 90 days.
Default to the shortest window that answers the question. Then choose the
smallest tool that can answer:

| Question | First tool | Bound |
| --- | --- | --- |
| Which route, provider or model costs most; spend with one provider or model; a daily trend | `metergraph_get_usage_aggregates` with `group_by` and exact `route`, `provider`, `model` or `environment` filters | `days` or `since`/`until`, small `limit` |
| Daily cost per route, when grouped usage is unavailable | `metergraph_get_usage` | `days`, small `limit` |
| Which routes exist or are replay eligible | `metergraph_list_routes` | none needed |
| Is data arriving | `metergraph_get_ingestion_health` | `days` |
| Known alert or anomaly | `metergraph_list_incidents` | small `limit` |
| Cost or calls for one prompt, workflow or other tag value | `metergraph_get_usage` with `metadata` (exact pairs), or `metergraph_get_usage_aggregates` with `group_by` including `metadata.<key>` | `days`, small `limit` |
| One failed, slow or costly call | `metergraph_query_traces` with `status`, `route`, `trace_id`, `request_id` or `metadata` | `limit` 1 to 5 |
| A finished analysis | `metergraph_list_reports`, then `metergraph_get_report` | small `limit` |

Use `metergraph_get_usage_aggregates` only when capabilities list
`usage_aggregates` as available. On an older deployment it is absent: say so,
answer what `metergraph_get_usage` can (cost per route and day), and do not
rebuild provider or model totals by paging traces.

### Cost questions

`metergraph_get_usage_aggregates` groups calls by any ordered subset of
`provider`, `model`, `route` and `day` (the call's UTC calendar day), plus at
most one `metadata.<key>`. Cost is
attributed per call, so a trace that used two providers adds each call's cost
to that call's provider. Groups come back highest cost first, at most `limit`
of them; `totals` cover every matching call whatever the limit. From a shell,
the `metergraph` CLI sends the same read and prints the same evidence. Check
`metergraph help usage` first: use these commands only when it lists
`--group-by`. An older CLI has only `metergraph usage --days N` (cost per route
and day); use the tool instead, or say a newer CLI is needed.

| Question | Tool arguments | CLI |
| --- | --- | --- |
| Most expensive route today | `{"group_by": ["route"], "days": 1}` | `metergraph usage --group-by route --today --json` |
| Spend with one provider | `{"group_by": ["provider"], "provider": ["<name>"], "days": 7}` | `metergraph usage --group-by provider --provider <name> --days 7 --json` |
| Spend by model | `{"group_by": ["model"], "days": 7}` | `metergraph usage --group-by model --days 7 --json` |
| One route's daily trend | `{"group_by": ["day"], "route": ["<route>"], "days": 14}` | `metergraph usage --route <route> --group-by day --days 14 --json` |
| Cost by prompt ID | `{"group_by": ["metadata.prompt_id"], "days": 7}` | `metergraph usage --group-by metadata.prompt_id --days 7 --json` |
| Today against yesterday | two reads: `days: 1`, then `since`/`until` for the prior UTC day | `metergraph usage --group-by route --today --compare previous --json` |

Rank only what was returned. When `coverage.rows.truncated` is true (more
groups matched than `limit`), a ranking by calls, errors or latency covers
only the listed groups; raise `limit` to `coverage.rows.matched` (at most 200)
or narrow the read before naming a "top" group. Name the latency you report:
`latency.avg_ms` is the mean over `latency.samples` calls that reported one,
and `latency.p95_ms` is an estimate from a fixed histogram
(`p95_method: histogram_estimate`), not an exact percentile.

A "costs most" answer needs exact pricing. When `pricing.cost` is
`lower_bound` (the overall `pricing`, or a group's own), some calls are not
fully priced, so a group with more unpriced calls can look cheaper than it is.
Name the group with the highest recorded cost as a lower bound and say the
ranking is not definitive until pricing is exact; never call it the most
expensive outright.

A prior-period comparison needs two reads with stated windows. Comparing
today so far with all of yesterday is not like for like: say so, or compare
with yesterday up to the same UTC time (`--compare previous-same-time` in the
CLI). A group missing from a truncated window is unknown, not zero.

A route is not a prompt. One route (for example `support-reply`) can carry
several prompt IDs in its metadata (SDK tags), so answer "which prompt costs
most" by grouping on the metadata key, not by route:

```json
{"name": "metergraph_get_usage_aggregates", "arguments": {"days": 7, "group_by": ["route", "metadata.prompt_id"]}}
{"name": "metergraph_query_traces", "arguments": {"route": "support-reply", "metadata": {"prompt_id": "reply-v3"}, "limit": 3}}
```

Metadata values are exact, case-sensitive opaque strings: `reply-v3` does not
match `reply-v30`, a call without the key never matches, and several keys must
all match. Calls without the key are the group whose value is `null`, and
`coverage.reasons` names `metadata_key_missing` (or `metadata_value_ineligible`
for a non-string or oversize value); say so rather than dropping them.
`metadata_groups.unlisted` accounts for every call not listed with a value:
`other_values` (values past the limit, with a group count), `missing_key` and
`ineligible_value`. Report the spend in `missing_key` plus `ineligible_value`
as not attributed to any value of the key, so a prompt ranking never reads as
the whole spend. When `coverage.rows.truncated` is true, the listed groups are
not the whole window: quote `totals` for the window and
`coverage.rows.matched` as the number of matched groups. That counts groups,
not distinct values of the key: with `group_by: ["route", "metadata.prompt_id"]`
one prompt used on three routes is three groups. For a count of distinct
values, read with the metadata key as the only dimension. From the CLI, the same
reads are `metergraph usage --group-by route,metadata.prompt_id --json`
(`--group-by-metadata prompt_id` is the same dimension, and the way to give a
key that contains a comma) and
`metergraph traces --metadata prompt_id=reply-v3 --json`.

Follow `next_cursor` only while you are still inside the agreed bound, and say
how many pages you read. Never request every trace, every report or unbounded
history.

## 3. Escalate privacy classes one step at a time

- Metadata tools answer most questions. Stay there unless the answer needs
  captured prompts, outputs, tool calls or report evidence.
- `metergraph_get_trace` and `metergraph_get_report_evidence` return captured
  content (`agent:read`). Ask the user before calling them, name the single trace
  or workload you will read, and do not quote more captured content than the
  answer needs. Never paste secrets you find in content.
- `metergraph_replay_trace` (`agent:replay`) sends a captured trace to a model
  provider and can spend money. It needs separate, explicit approval that names
  the trace, the overrides and the timeout. Replay is non-persistent: it does not
  change production telemetry, prove a fix or substitute for an evaluation run.

Read access never grants evaluation writes, analysis launch, dashboard changes,
key rotation or production configuration changes. Refuse those requests and
point to the human action in the Metergraph app instead.

## 4. Answer only from returned evidence

Every answer cites, from the tool responses you actually received:

- **Workspace**: workspace name and `provenance.workspace_id`, plus
  `deployment_profile`.
- **Window**: `window.since` to `window.until` in UTC (or `days`) for each
  read, and whether the last day is partial.
- **Provenance**: the tool name, `provenance.source` and `generated_at`.
- **Evidence and completeness**: `evidence.rows`, `evidence.complete`,
  `page.truncated` and whether a `next_cursor` was left unread; for usage,
  `coverage.completeness` with its `reasons`, `coverage.rows.matched` against
  the rows returned, and whether a total is the whole population
  (`totals.scope`) or only the returned rows.
- **Pricing and attribution**: `pricing.cost` (`exact` or a `lower_bound`) and
  `attribution.level`. A trace cost is a whole-trace total and is never split
  by provider.
- **Warnings**: every returned `warnings[].code` with its message. Say "no
  warnings returned" when the list is empty.
- **Identifiers and links**: trace, request, incident or analysis IDs, and
  `metergraph_links` values exactly as returned. Never construct a link.

Keep these states distinct and name the one that applies: no data in the
window, incomplete or truncated evidence, capability unavailable in this
deployment, classification pending, ambiguous request match
(`request_match.ambiguous`), failed analysis, and missing report. An empty page
does not prove there was no traffic; check ingestion health or a longer bounded
window before saying so. Do not round, extrapolate or invent totals. Never
attribute a cost change, or the absence of one, to a code change from source
code or a git diff; see section 5.

## 5. Code changes and cost: never decide from the diff

When the question is whether a commit, pull request, deploy or config change
raised, lowered or did not change cost, a git diff is never the evidence. Read
it to form a hypothesis (a different model, a longer prompt, a new retry loop, a
changed `max_tokens`, an added tool call), then say it is a hypothesis. Do not
answer "this commit increased cost", "this commit saved money" or "this commit
has no cost impact" from code alone, including a diff that touches no model or
prompt code: wrappers, retries, caching, routing, traffic and provider prices
change spend without appearing in the diff.

A cost conclusion needs returned Metergraph usage evidence:

1. Establish when the change reached the traffic Metergraph observes, from
   recorded commit or deployment identity (a deploy record, or the commit the
   telemetry itself carries). Merge time is not deploy time. Without that
   record, any before-and-after reading is only a time correlation: call it
   that, give the windows, and do not attribute the difference to the commit.
   If no one knows when it shipped, say the comparison cannot be anchored.
2. Read usage for the same route or workload over comparable, bounded UTC
   windows before and after that point (`metergraph_get_usage_aggregates`
   with explicit `since` and `until` and the same filters, or
   `metergraph_get_usage` where grouped usage is unavailable), and cite both
   reads as in section 4. Windows of equal length avoid comparing a partial
   day with a whole one. Filter both reads to the environment the deployment
   record names (`environment`), so traffic in another environment that
   shares the route is not credited to the change. If that environment
   cannot be isolated (for example the grant or deployment has no
   environment filter), say the cost impact is unknown.
3. Compare per-call cost and token counts as well as totals, so a traffic
   change is not mistaken for a code change. Name what else changed in the
   window when you know it (traffic, provider prices, other deploys).
4. If either window is incomplete, truncated or warned, if the windows are not
   comparable, or if the returned data cannot separate traffic by the change,
   state that the cost impact is unknown and name the next bounded check. Do
   not fill the gap from the diff.

Present the diff and the usage evidence separately: what the code suggests,
and what Metergraph measured.

## 6. Worked workflow: one failed trace

1. Discover: context, then capabilities. Confirm the workspace with the user.
2. Find: `metergraph_query_traces` with `status` set to the failure status, the
   agreed `days` and `limit` 1. If the user gave a request ID and the match is
   ambiguous, list the candidates and ask which one.
3. Explain from metadata: route, model, provider, tokens, cost, latency, status
   and span count, with the citations above. If metadata is enough, stop here.
4. Optional content: with consent, `metergraph_get_trace` for that one trace to
   read the error, tool calls and root-cause classification.
5. Optional replay: only with explicit approval and when the trace is replay
   eligible, run one bounded `metergraph_replay_trace`, report the returned
   status and comparison, and state that nothing in production changed.
6. Close with what is known, what is unknown, and the next bounded check.
