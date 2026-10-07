# Known issues

This document lists known limitations of the live group, their workarounds, and what is **not** a known issue (yet).

## Orphaned skill-call warning

**Status:** documented and mitigated, **not** resolved.

**What happens.** During `Scout ∥ Hunter` (parallel discovery), LobeHub may print warnings of the form:

> Обнаружен осиротевший вызов навыка.

**Root cause (confirmed).** The runtime binds tool-call results **positionally** within one assistant turn. Batches of 2+ tool calls in the same turn, while running in parallel with another agent, cause:

- result-to-slot mismatch,
- a skill call left without a result (`PARALLEL_RACE`),
- a primary call that fails plus a fallback call in the same turn (`FALLBACK_ORPHAN`).

**Mitigation (in this release).** Section 57 of the group prompt enforces `ONE-CALL-PER-TURN` and `CLOSE-THEN-FALLBACK` for every field agent. Section 58 enforces `NO DUPLICATE DISPATCH`. Section 31 reinforces the same.

**Workaround (if it still happens).** Switch to `STABLE MODE`:

```
Scout → Hunter → Analyst → Fact Checker → Synthesizer
```

Reliability > speed. Do not claim the warning is "definitely not" caused by this protocol unless the root cause has been independently confirmed.

## Analyst timeout

**Status:** known regression, mitigated by `ANALYST DEGRADED` fallback.

**What happened.** In earlier runs, the Analyst timed out and the Supervisor silently assembled a "Evidence Ledger" itself, bypassing the protocol.

**Mitigation (in this release).**

- Section 25 / 62 / 26 / 36 explicitly forbid the Supervisor from impersonating the Analyst.
- The Analyst retry chain is bounded and labeled.
- A `DEGRADED` bridge package is allowed only as a typed table (`FIELD | VALUE | TYPE | STATUS | CONFIDENCE | SOURCE`) and is explicitly marked `ANALYST_STATUS: DEGRADED` in the Research Audit.
- The Fact Checker is mandatory notified and is forbidden from raising the confidence of a degraded artifact.

## Self-reported benchmarks

**Status:** environmental risk, not a defect.

**Why it matters.** Authors of competing tools often publish their own benchmarks. The format rarely matches competitor methodology, datasets, or evaluation metrics. Direct ranking from self-reported numbers is misleading.

**Mitigation (in this release).**

- The Evidence Ledger requires `BENCHMARK NORMALIZATION` (one task? one dataset? same conditions? same metric? comparable model class?) before any ranking is allowed.
- Otherwise the comparison is marked `BENCHMARK NOT COMPARABLE`.
- Self-reported numbers are explicitly tagged `SELF-REPORTED BENCHMARK`.

## "Windowsy" / "local" semantics

**Status:** environmental risk, mitigated by classification contract.

**Why it matters.** "Works on Windows" can mean native installer, WSL, Docker Desktop, Web only. Collapsing them to a single boolean breaks user decisions.

**Mitigation (in this release).** The Evidence Ledger requires a separate classification:

| Plane | Possible values |
|---|---|
| `APP_HOSTING` | `NATIVE_INSTALLER` · `DIRECT_RUNTIME` · `DOCKER_DESKTOP` · `WSL` · `WEB_ONLY` · `NOT_VERIFIED` |
| `LLM_INFERENCE` | local Ollama · LM Studio · cloud API · multiple |
| `SEARCH_BACKEND` | local SearXNG · cloud API · multiple |
| `DATA_STORAGE` | local SQLite · managed DB · multiple |

Default for "README does not mention WSL" is `WSL: NOT DOCUMENTED`, **not** `WSL: NO`.

## Missing MCP server support in some RAGs

**Status:** environmental risk; document varies by tool.

**Why it matters.** Not every RAG tool in the live config supports the Model Context Protocol. The Synthesizer should mark `MCP: NATIVE` / `EMULATED` / `NOT SUPPORTED` based on the actual feature, not on claims.

## Stale GitHub data

**Status:** known pitfall, mitigated by semantic naming.

**Why it matters.** `pushed_at` is **not** `LAST_COMMIT`. The protocol names them separately:

| API field | Variable |
|---|---|
| `pushed_at` | `LAST_PUSH` |
| `updated_at` | `REPO_UPDATED_AT` |
| `stargazers_count` | `STARS` |
| `open_issues_count` | `OPEN_ISSUES` |
| `archived` | `ARCHIVED` |
| `license` | `API_LICENSE` |
| `LAST_COMMIT` | only from `commits` API on default branch |

## Documentation parity

**Status:** intentional.

- `agents/curator.md` etc. are **live exports** of the live system prompts. They are not abbreviated "ideas" of the agents.
- The Markdown summary in each `agents/*.md` describes the role, the recommended model profile, the required/optional tools, and the boundaries.
- The full live prompt is the fenced block. If you copy-paste only the fenced block into LobeHub, you get the live agent.

If you find a divergence between the fenced block and the live runtime, please open an issue.