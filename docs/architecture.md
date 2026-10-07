# Architecture

DEEP RESEARCH SWARM is a multi-agent research pipeline for LobeHub. It separates the jobs that most "research agents" cram into a single system prompt:

- search and discovery,
- primary-source verification,
- deep reading and evidence extraction,
- contradiction hunting,
- and writing the final answer.

This separation is not decorative. It exists because each one rewards a different model and a different toolset. The point is not to maximize the number of agents — the point is to create a **disciplined evidence pipeline** that can:

- fan out across the web, GitHub, forums, papers and official docs;
- prefer primary sources over summaries;
- keep claims tied to provenance;
- distinguish facts, source claims, community signals and hypotheses;
- detect contradictions instead of smoothing them over;
- run targeted second-pass verification when evidence is weak;
- return **one coherent final answer with real citations**.

## The pipeline

```
USER
  ↓
CURATOR / SUPERVISOR
  ├─ understands the question, picks a mode (QUICK / STANDARD / DEEP / MAX / ULTRA)
  ├─ writes a SEARCH_PROGRAM (goal, modes, languages, source types, candidate counts)
  ├─ dispatches workstreams to Scout ∥ Hunter
  ├─ runs RETRIEVAL JUDGE / PROGRESSIVE RERANKING
  ├─ asks the Analyst for the Evidence Ledger
  ├─ asks the Fact Checker to break the conclusions
  ├─ if FAIL → targeted verification → loop
  └─ if PASS → asks the Synthesizer for ONE FINAL ANSWER
```

![Architecture](../assets/architecture.svg)

## The six agents

| Agent | Mission | Output |
|---|---|---|
| **Curator / Research Director** | Plans, routes, controls depth, merges evidence | research plan, workstreams, final call |
| **Wide Web Scout** | Finds the broad candidate space | ranked candidate pool + discovery map |
| **Primary Source Hunter** | Goes after official docs / repos / papers / releases | provenance-first candidate list with URLs |
| **Evidence Analyst** | Deep reads, extracts passages, builds the ledger | Evidence Ledger + Claim/Entity/Source graphs |
| **Fact Checker / Red Team** | Tries to **disprove** the candidate conclusions, runs the blocking Quality Gate | PASS/FAIL with gap extraction |
| **Research Synthesizer** | Writes the one final answer | single-message Markdown report with claim-level citations |

Each agent has its own live system prompt exported from the production group. See `agents/*.md`.

## Why a star topology

Only the Curator speaks to the user. Specialists return their work to the Curator; they never recursively delegate to one another. This:

- avoids loops (A → B → A → B),
- keeps the Fact Checker independent of the strategy that produced the draft,
- makes the pipeline easy to debug,
- lets the Curator reason about tool budgets without violating each agent's boundaries.

## The Quality Gate is a hard gate

The Synthesizer is **technically forbidden** until the Fact Checker returns `PASS`. A `FAIL` triggers a new round of targeted verification. The Curator cannot:

- lower the gate ("the source looks fine, just write the answer"),
- substitute itself for the Fact Checker,
- or merge `FAIL` and `PASS` and proceed.

This is what makes the system a research system rather than a search-and-blurb engine.

## Mode ladder

The system scales effort to the question.

| Question type | Mode |
|---|---|
| latest version, single fact, one number | ⚡ QUICK |
| "compare X and Y" | 🔹 STANDARD |
| "find best alternatives" / "study deeply" / a decision | 🔎 DEEP |
| "study the market" / "scrape the internet" | 🧠 MAX |
| "deepest possible + try to refute" | 🧬 ULTRA |

See `group/research-modes.md` for the full ladder and the auto-selection heuristics.

## What this is NOT

- Not a hosted service.
- Not an official LobeHub product.
- Not a replacement for a human researcher — it is a research aid that follows evidence-first discipline and a mandatory Quality Gate.
- Not a single-prompt "deep research" hack — the depth here comes from the pipeline, not from a 5 KB system prompt.