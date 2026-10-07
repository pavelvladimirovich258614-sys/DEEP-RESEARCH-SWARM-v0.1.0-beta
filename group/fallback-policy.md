# Fallback & retry policy

This file describes how the Curator recovers when a specialist stalls, errors, or returns degraded output. It encodes section 25, 26 and 62 of the live group prompt.

## 1. Time-boxed retries

Every field agent has a bounded retry chain. The Curator never waits forever.

| Agent | Retry chain |
|---|---|
| Scout / Hunter | 1 retry on technical error |
| Evidence Analyst | retry → reduced-scope retry → split into 2–3 chunks with merge → DEGRADED fallback |
| Fact Checker | 1 retry |
| Synthesizer | retry only if the output was technically truncated |

The same task may not be retried more than twice. After two failures, status becomes `DEGRADED` and the Curator chooses:

- `REASSIGN` — send to a different agent or use the same agent with a smaller scope;
- `REDUCE SCOPE` — narrow the workstream to a smaller deliverable;
- `CONTINUE WITH CAVEAT` — proceed but flag the gap in the final report;
- `STOP` — abort the run and explain why.

The choice and the reason are recorded in the Research Audit section of the final report.

## 2. Analyst DEGRADED fallback (most common pitfall)

**The Curator MUST NOT impersonate Analyst. There is no fallback where the Curator "just compiles the evidence ledger itself."**

If the Analyst retry chain is exhausted:

1. `ANALYST_STATUS = DEGRADED` is set.
2. The Curator MAY produce a **minimal bridge package**: a table with the rows `FIELD | VALUE | TYPE | STATUS | CONFIDENCE | SOURCE` — without re-evaluating evidence, creating new facts, raising confidence, rewording claims, or replacing the Analyst.
3. The Fact Checker is **mandatorily** informed: `ANALYST_STATUS = DEGRADED`. The Fact Checker must not promote the status/confidence of a degraded artifact. If it has any doubt → FAIL or `NOT VERIFIED`.
4. The final Research Audit records `ANALYST_STATUS: DEGRADED` and explains what exactly was degraded.

This rule fixes the documented regression in which the live Analyst timed out and was silently replaced by a Supervisor-led Evidence Ledger.

## 3. SEQUENTIAL TOOL CALLS (orphan-fix)

Inside the parallel phase (Scout ∥ Hunter), each agent must:

- Issue at most **one** tool/skill call per assistant turn.
- Wait for the result before issuing the next call.
- **CLOSE-THEN-FALLBACK** — when a primary call degrades (`FORBIDDEN`, `403`, `429`, "Do not retry this call, switch tools", timeout), the agent first closes the primary call with its terminal result (even if it's an error), THEN runs the fallback in a SEPARATE next turn.
- If a tool call is observed without a result, the agent ends the turn **without** further tool calls, and retries the call solo in the next turn.

Returning to "batch tool calls" while running in parallel with another agent is prohibited because of the positional runtime race that produces "orphaned skill call" warnings.

## 4. FAILURE ADAPTATION (search-layer)

When a search strategy fails, the Curator tries the next strategy in this list, in order:

1. query rewrite;
2. language switch;
3. source type switch;
4. exact phrase (lexical / quoted);
5. site search;
6. alternative domain;
7. official repo / changelog;
8. community source.

It does **not** keep retrying the same call.

## 5. Dead-link recovery

A dead URL is not a valid citation. The Curator:

- searches for an updated docs URL, a GitHub source, or an official mirror;
- marks the citation as `DEAD_LINK` plus a recovery status;
- prefers archive.org only when no canonical source exists.

## 6. Tool budget

The Curator tracks `SEARCH_CALLS`, `PAGE_OPENS`, `DEEP_READS`, `RESEARCH_ROUNDS`. It does **not** open 200 pages when 25 authoritative sources already close the question.

## 7. STOP RULE

The research run ends when **all** of the following are true:

- the user's question is answered;
- top candidates are confirmed;
- critical facts are verified;
- Fact Checker returned `PASS`;
- remaining gaps do not change the recommendation;
- search saturation is reached (`NEW_CLAIM_RATE`, `NEW_PRIMARY_SOURCE_RATE`, `NEW_CONTRADICTION_RATE`, `NEW_CANDIDATE_RATE`, `GAP_CLOSURE_RATE` all near zero).

Absolute completeness is not required. A `NOT VERIFIED` gap is a legitimate outcome.