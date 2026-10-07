# Troubleshooting

This document covers the failure modes observed in real runs. Most of them are upstream-protocol violations; the fix is to re-paste the prompt verbatim from this repository.

## 1. "Orphaned skill call" warning

**Symptom.** During the parallel phase, LobeHub prints warnings like:

> Обнаружен осиротевший вызов навыка.

**Root cause.** Parallel agents issuing batches of tool calls in the same turn. The result is positioned by slot, not by stable id, so when Scout and Hunter run together the second call's result lands in the first call's slot. The remaining skill call shows up as "orphaned".

**Fix.**

1. Re-paste the group prompt verbatim from `group/group-prompt-raw.txt` — do **not** paraphrase; the `SEQUENTIAL TOOL CALLS` rule lives inside sections 57–59.
2. Make sure each specialist agent's prompt is also verbatim, in particular the `TASK BOUNDARIES` line of the delegation contract.
3. If the warning still appears, switch to **STABLE MODE** (sequential):

```
Scout → Hunter → Analyst → Fact Checker → Synthesizer
```

Reliability > speed. The runtime warning is documented; do not claim it is "definitely not" caused by this protocol.

## 2. Agent not called

**Symptom.** The user asks a question and the Supervisor answers directly without delegating.

**Fix.**

1. Re-paste the Curator prompt verbatim from `agents/curator.md`. The protocol that says "you do not write the final answer, the Synthesizer does" lives inside that prompt.
2. Confirm the Supervisor is configured with the right tools (`lobe-web-browsing`, `lobe-agent-management`).

## 3. Tool unavailable

**Symptom.** A specialist tries to use a plugin that is not enabled for its profile.

**Fix.**

- Add the missing plugin to that agent only.
- For platform limitations, the protocol explicitly distinguishes `NATIVE` / `EMULATED` / `NOT SUPPORTED`. Do not invent a tool.

## 4. Search loops

**Symptom.** The same query is sent 5+ times without progress.

**Fix.** The protocol's `FAILURE ADAPTATION` ladder says: do **not** repeat the same call. Try in this order:

1. query rewrite,
2. language switch,
3. source type switch,
4. exact phrase (lexical / quoted),
5. site search,
6. alternative domain,
7. official repo / changelog,
8. community source.

If after step 8 the gap is still open, mark it `NOT VERIFIED` and move on. Use the gap budget, not infinite retries.

## 5. Excessive context

**Symptom.** The Synthesizer writes something that contradicts earlier messages.

**Fix.**

- Always start a fresh conversation for deep research.
- Cap page openings. The protocol's `TOOL BUDGET` says: do not open 200 pages when 25 close the question.
- Use `lobe-agent-documents` to persist the Evidence Ledger, not the conversation context.

## 6. Timeouts

**Symptom.** A specialist returns no response after a long wait.

**Fix.** The `TIMEOUT / RETRY POLICY` says:

- Scout / Hunter: 1 retry on technical error.
- Analyst: retry → reduced-scope retry → chunk-split → DEGRADED fallback.
- Fact Checker: 1 retry.
- Synthesizer: retry only if the output was truncated.

If the Analyst times out twice, do **not** impersonate it. Build a minimal bridge package with the rows you already have, set `ANALYST_STATUS = DEGRADED`, and let the Fact Checker know.

## 7. Failed specialist

**Symptom.** A specialist returns degraded output (truncated, contradiction-heavy, off-protocol).

**Fix.**

- Re-issue the contract with `RETRY` labelled explicitly.
- If still degraded, `REDUCE SCOPE` to a smaller deliverable.
- Never merge `FAIL` and `PASS` to keep going.

## 8. Incomplete citations

**Symptom.** The Synthesizer's draft has claims without URLs.

**Fix.**

- Re-paste the group prompt verbatim. The citation policy lives in the prompt.
- Ask the Analyst to re-extract relevant passages for the missing claims.
- Do **not** have the Synthesizer fill in citations from memory.

## 9. Stale GitHub data

**Symptom.** The report says "no commits in 12 months" but `pushed_at` was last week.

**Fix.** The protocol separates `pushed_at` (`LAST_PUSH`) from `commits` API (`LAST_COMMIT`). They are not the same. Use the right label:

- `LAST_PUSH` is from `pushed_at`.
- `LAST_COMMIT` is only the commits API on the default branch.

If only `pushed_at` is known, write "no push in N months", **not** "no commits".

## 10. Model tool-calling failure

**Symptom.** The model returns tool calls that don't match its schema.

**Fix.**

- This is usually a model-version issue. Switch provider/model, or reduce tool set.
- Do not paper over by replacing the model with a hand-coded workflow. That is a refactor of the live system and requires explicit user authorization.

## 11. Parallel execution instability

**Symptom.** Scout and Hunter seem to interact or one overwrites the other.

**Fix.**

- Ensure `NO DUPLICATE DISPATCH` is enforced (one workstream = one dispatch).
- Ensure each agent respects `ONE-CALL-PER-TURN` in parallel phase.
- If still unstable, switch to `STABLE MODE` (sequential).

## 12. Two different model policies

**Symptom.** The Curator uses `mistral-large-4` while the rest use `MiniMax-M3`; or similar drift over time.

**Fix.** This is not a bug, it's a feature. Different agents benefit from different model strengths. If you decide to change a model's role, follow the **Конфигурация неприкосновенна** rule (group prompt section 72): changes are allowed only for (1) real bugs, (2) important new features, or (3) LobeHub-version incompatibility. Do not change models casually.

## 13. What to do when nothing fixes

Open an issue on GitHub. Include:

- the conversation ID (no agent IDs, no user IDs),
- the mode (`QUICK` / `STANDARD` / `DEEP` / `MAX` / `ULTRA`),
- the failing agent,
- the last 3 lines of the Fact Checker verdict (if any),
- the model provider used by each agent.

Do not paste API keys, tokens, or account identifiers.