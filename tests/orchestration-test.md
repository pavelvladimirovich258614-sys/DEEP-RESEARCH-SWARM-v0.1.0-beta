# Orchestration test

Validates that the **Supervisor-controlled star topology** is intact and that the specialists do not recursively call one another.

## What to test

```
[ ] Curator never says "I will write the answer myself" — it always
    delegates to specialists
[ ] Wide Web Scout reports on a CANDIDATE POOL table, not on a final answer
[ ] Primary Source Hunter returns provenance-first URLs
[ ] Evidence Analyst reports CLAIM LEDGER rows
[ ] Fact Checker reports a VERDICT (PASS / FAIL)
[ ] Research Synthesizer is invoked ONLY after PASS
[ ] On FAIL, the Curator dispatches targeted tasks and the loop continues
[ ] The final answer is ONE message (no workstream-by-workstream dump)
```

## How to run it

1. Start a fresh conversation in the group.
2. Run a `🔎 DEEP` question with a known contradiction (e.g., "is X faster than Y?" when community reports disagree).
3. Watch the progress stages: `Planning → Discovery → Primary sources → Reranking / deep reading → Gap closure → Evidence analysis → Fact check → Final synthesis`.
4. Verify the table above.

## Star-topology assertions

- the Curator never forwards work to Synthesizer before the Fact Checker returns PASS.
- the Fact Checker does not consult the Scout or Hunter after receiving the Evidence Ledger — it only inspects the ledger.
- the Synthesizer does not run a search — it only consumes the Evidence Ledger and the Fact Checker verdict.
- no agent invokes another agent except via the Curator.

If any assertion fails, re-paste the relevant prompt verbatim and re-run.

## Orphan-fix smoke test

Ask a question that triggers `Scout ∥ Hunter` parallel discovery.

Expected:

- no "orphaned skill call" warnings;
- if the warning appears, switch to `STABLE MODE` (`Scout → Hunter → Analyst → Fact Checker → Synthesizer`) and re-run.

See [`docs/known-issues.md`](../docs/known-issues.md) for the rationale.