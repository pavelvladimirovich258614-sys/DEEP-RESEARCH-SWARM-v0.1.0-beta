# Research benchmark

Measures how well the swarm answers genuinely hard research questions.

**This directory exists so that prompts get changed on evidence, not on vibes.**
The order is fixed: MEASURE → FIND FAILURE → FIX ONE THING → RETEST. Do not rewrite
agent prompts because a run scored badly. Score first.

## Layout

```
benchmark.json          15 tasks, machine-readable
rubric.md               the 13 metrics, with scoring rules
run-template/           metrics.json + evaluation.md to copy per run
tools/evaluate_run.py   mechanical counters for a completed run
```

Runtime output goes to `benchmark-results/` at the repository root and is deliberately
**not** committed — it is per-installation, contains transcripts, and will contain
real URLs and possibly account-specific detail.

## Why these tasks

Every task is built so that one search query cannot answer it. Each requires combining
several source classes, and several contain a deliberate trap:

- **BR-07** states a false premise. The swarm must refute it from a primary source
  instead of researching the premise.
- **BR-10** gives conflicting benchmark numbers that differ for methodological reasons.
- **BR-14** will tempt the swarm into citing the original paper as its own replication.
- **BR-08** mixes three incidents that are frequently conflated.

The trap column exists so the Fact Checker has something concrete to attack.

## Running one task

1. Copy `run-template/` to `benchmark-results/run-NNN/`.
2. Paste the task `query` verbatim into a **fresh** group conversation. Do not reuse a
   conversation that already has research context — contamination makes runs incomparable.
3. Save each agent's output as `agent-<role>.md` and the final answer as `group-result.md`.
   Save the question as `query.txt`. These are the inputs `evaluate_run.py` consumes.
4. Record timings in `timings.json` if the platform exposes them:

   ```json
   {"total": 71.2, "agents": {"scout": 12.3, "hunter": 14.8}}
   ```

5. Run the counters:

   ```bash
   python tests/research-benchmark/tools/evaluate_run.py benchmark-results/run-NNN --out metrics.json
   ```

6. Fill in `evaluation.md` by hand for the metrics the script cannot judge.

## What the script does and does not do

Computes: source diversity, duplication and agent overlap, per-agent source counts,
source class heuristics, hallucination *candidates*, and passes through timings.

Does **not** compute: coverage, factuality, contradiction handling, synthesis quality,
citation entailment, failure recovery. Those need a reader. The script prints them under
`not_computed_here` so a run is never mistaken for fully scored.

## Honesty rules

These matter more than any score.

- `urls_in_final_not_in_agents` are **candidates**, not proven hallucinations. A citation
  written during synthesis that no agent produced is the classic signature, but verify
  each one before recording a metric 5 failure.
- Token counts stay `null` unless the platform returns them. Never estimate them from
  text length — a fabricated number gets compared across runs and then drives decisions.
- An UNKNOWN is a real result. Record it as UNKNOWN, do not round it to PASS.
- Do not average the 13 metrics into one composite number.

## Verifying the tooling

```bash
python tests/research-benchmark/tools/evaluate_run.py --self-test
```

Runs a synthetic fixture with no network and no LLM calls. It is a sanity check on the
counters, not a substitute for running the benchmark.