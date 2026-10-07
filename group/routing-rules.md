# Routing rules

This file describes how the Curator/Supervisor dispatches work to the six agents. The full live group prompt (where routing rules are encoded inline) lives in [`group-prompt.md`](group-prompt.md) and [`group-prompt-raw.txt`](group-prompt-raw.txt).

## 1. Star topology

Only the Curator/Supervisor speaks to the user. Specialists return their work to the Curator; they never recursively delegate to one another.

```
USER → CURATOR (Supervisor)
   ↓
SC ∥ H → A → FC → (PASS/FAIL) → S → FINAL
```

Where `SC = Scout`, `H = Hunter`, `A = Analyst`, `FC = Fact Checker`, `S = Synthesizer`.

## 2. Delegation contract (4 fields)

Every dispatch from the Curator to a field agent MUST carry four fields:

| Field | Meaning |
|---|---|
| `OBJECTIVE` | What this workstream must produce, written as a single decision question |
| `OUTPUT FORMAT` | The exact shape of the response (candidate pool table, evidence ledger rows, claim graph, …) |
| `TOOLS / SOURCES GUIDANCE` | Which tools the agent should prefer, which sources to prioritize, which to downrank |
| `TASK BOUNDARIES` | What it must NOT do; in particular the `SEQUENTIAL TOOL CALLS` rule (one tool call per turn inside the parallel phase) |

This contract is the same shape used by Anthropic's "multi-agent research" orchestration and avoids recursive delegation.

## 3. Routing heuristics

| Need | Route to | Why |
|---|---|---|
| Broad internet discovery, multi-language, communities | **Wide Web Scout** | wide net, query fan-out |
| Official docs, GitHub repo/releases/issues, papers, filings, release notes | **Primary Source Hunter** | provenance-first |
| Deep reading, passages, evidence ledger | **Evidence Analyst** | owns the ledger |
| Contradiction search, citation audit, repository health, version awareness | **Fact Checker / Red Team** | adversarial reviewer |
| Final answer with citations | **Research Synthesizer** | writes the final report |
| Tactical decisions (which tool, which model, which mode) | **Curator** | orchestration only |

## 4. NO DUPLICATE DISPATCH

- One workstream = one active dispatch.
- The Curator never re-sends the same workstream contract until the previous response is received or the dispatch is explicitly marked `LOST`.
- Retry is always labelled `RETRY` / `RETRY #2` / `REDUCED RETRY` so it cannot be mistaken for an independent task.

## 5. SEQUENTIAL TOOL CALLS (orphan-fix)

Inside the parallel phase (Scout ∥ Hunter), each agent must:

- Issue at most one tool/skill call per assistant turn.
- Wait for the result before issuing the next call.
- Close a failed primary call with its terminal result (even if it's an error) BEFORE switching to a fallback.
- Never batch 2–9 tool calls in a single message while running in parallel with another agent.

This is what prevents the "orphaned skill call" runtime warning observed on some LobeHub runs.

## 6. Contradiction handling

If Hunter returns fact A and Scout returns fact not-A, the Curator does **not** pick a side. The Fact Checker is dispatched as an independent reviewer with both sides. The Fact Checker returns:

- which side has stronger evidence,
- which source is the origin,
- which version/date is involved,
- whether further search is needed.

Only the Fact Checker's verdict moves the chain forward.