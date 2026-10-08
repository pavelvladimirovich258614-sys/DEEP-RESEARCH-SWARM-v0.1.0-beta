# Swarm evaluation rubric

How to score a single research run. Every metric below is defined so that two people
scoring the same run should land on the same verdict, and so that as many metrics as
possible can be counted mechanically by `tools/evaluate_run.py`.

Scoring convention:

- **PASS / FAIL** — binary, checkable against the artifact.
- **0–3** — ordinal scale, defined per metric. Do not invent intermediate scores.
- **UNKNOWN** — the run did not provide enough evidence. This is a legitimate result
  and must be recorded rather than silently rounded to PASS.

An UNKNOWN is never rounded to PASS. If the swarm cannot show its work, the metric
did not pass.

---

## 1. COVERAGE

Did the answer actually cover the question that was asked, including its negative space?

- 3 — every sub-question in `benchmark.json:required_signals` addressed; scope matches the
  query; the answer states what it did not cover.
- 2 — main sub-questions covered; one secondary part thin.
- 1 — a major sub-question is missing or the answer drifted in scope.
- 0 — the question was not answered.
- FAIL if the final report omits a required signal the task explicitly demanded.

Check by mapping each `required_signal` to a location in the final report.

## 2. SOURCE QUALITY

Count sources by class, using the project's own ledger taxonomy
(`CLASS = PRIMARY / SECONDARY / COMMUNITY`).

- Record `primary`, `secondary`, `community` counts.
- FAIL if any critical claim rests only on COMMUNITY class.
- FAIL if a claim cites only a search snippet as supporting evidence. Snippet is
  discovery evidence only, per the group prompt.
- 3 — every load-bearing claim has a PRIMARY source.
- 2 — some claims rely on good SECONDARY sources.
- 1 — load-bearing claims rest on weak sources.
- 0 — sources are undifferentiated or unciteable.

## 3. SOURCE DIVERSITY

Did the swarm read broadly, or harvest everything from one or two sites?

- FAIL if `unique_domains <= 2` for any task above difficulty 2.
- 3 — sources span primary docs, code repositories, and at least one independent or
  critical voice.
- 2 — 3–5 domains, all of one flavour.
- 1 — effectively two sources with many pages.

Computed mechanically as `unique_domains` from URLs across all agent outputs.

## 4. FACTUALITY

Are claims supported at the level they are stated?

- Check every numeric claim, version, date and named entity against its citation.
- 3 — every checkable claim carries a claim-level citation that supports it.
- 1 — some claims supported, some merely adjacent.
- 0 / FAIL — claims stated with no citation.

## 5. HALLUCINATION RISK

This is the highest-severity metric. Treat any hit as a defect, not a deduction.

Look specifically for invented:

- URLs that were never opened or never appeared in any agent output;
- products, versions or release numbers that do not exist;
- prices, figures or measurements with no source;
- quotations attributed to a named person or document;
- APIs, papers or changelog entries that cannot be located.

- 3 — zero fabricated artifacts; every URL in the final report traces back to an agent output.
- 0 / FAIL — one or more fabricated URLs, products, versions, figures or quotes.

Mechanical pre-check: any URL in the final report that does not appear in any agent
output is a candidate hallucination. Verify each candidate before recording it.
A citation added during synthesis that no agent produced is the classic signature.

## 6. CONTRADICTION HANDLING

Did the swarm notice sources disagreeing, and did it resolve rather than average?

- 3 — contradictions surfaced, both sides cited, resolution reasoned, residual
  uncertainty stated.
- 2 — contradiction noticed but resolved by picking a side without evidence.
- 1 — contradiction silently dropped.
- 0 — a contradiction is stated as settled fact.

Tasks BR-07, BR-08 and BR-10 exist specifically to test this metric.

## 7. AGENT SPECIALIZATION

Did the six agents do different work, or did all six run the same search?

Map each agent's output to its intended role. Intended split:

- Curator — plan, mode selection, dispatch, gap decisions. Should produce no findings itself.
- Wide Web Scout — discovery breadth, candidate pool.
- Primary Source Hunter — official docs, repos, papers, filings.
- Evidence Analyst — ledger and claim/entity/source graph construction.
- Fact Checker / Red Team — disconfirmation, contradiction search, gate verdict.
- Research Synthesizer — final answer only.

- 3 — every agent's output is distinct and matches its role.
- 2 — minor overlap, roles still identifiable.
- 1 — 2+ agents produced interchangeable output.
- 0 / FAIL — six agents produced substantially the same content.

**The Curator producing research findings is a spec violation**, not a bonus:
the group prompt gives the Curator planning and dispatch, not search.

## 8. DUPLICATION

Measure overlap between agent outputs rather than describing it.

- Count URLs appearing in more than one agent's output.
- `duplicate_sources` in `metrics.json` is this count.
- 3 — minimal overlap; each agent contributes distinct material.
- 1 — heavy repetition of the same sources across agents.
- 0 / FAIL — duplication so high that parallel work was wasted.

High duplication is expected between Scout and Hunter by design, because Hunter
validates what Scout found. Duplication between Fact Checker and any discovery agent
is not expected.

## 9. FINAL SYNTHESIS

- 3 — answer is organised by the question's logic, not by agent; conflicts reconciled;
  citations attached to claims; no new facts introduced.
- 2 — well-structured but organised agent-by-agent, which reads as a relay rather
  than an answer.
- 1 — shallow restatement of agent outputs.
- 0 / FAIL — final answer missing, or produced despite a Fact Checker FAIL.

## 10. CITATION QUALITY

For each citation, walk the project's own verification chain: URL exists → page was
actually opened → page contains the claimed content → version matches → date relevant
→ not a repost of another source.

- 3 — spot-checkable citations that pass every step.
- 2 — citations resolve but entailment was not always verified.
- 1 — link-only citations with no passage-level support.
- 0 / FAIL — citations that do not support the claim, or fabricated URLs.

## 11. COST

- Leave `input_tokens` / `output_tokens` as `null` if the platform does not return them.
- Do not estimate token counts from text length. A fabricated number is worse than a
  missing one, because it will be compared across runs and used for decisions.
- When available, record cost per successful run so quality-per-token can be tracked.

## 12. SPEED

- `runtime_seconds` total, plus per-agent runtime when the platform exposes it.
- Note the mode used. A ULTRA run taking four times a STANDARD run is not a defect.
- A FAST run taking as long as a MAX run suggests the mode ladder is not actually
  changing behaviour.

## 13. FAILURE RECOVERY

Score what the swarm did when things went wrong, not whether something went wrong.

Probe:

| Injected failure | Expected behaviour |
|---|---|
| Source unreachable | Mark SNIPPET-ONLY, lower confidence, continue — no fabrication |
| Search returns nothing | Report the empty result, broaden query, do not fill the gap |
| One agent errors | Curator re-dispatches or degrades explicitly, never silently drops a workstream |
| Sources contradict | Route to Fact Checker, do not average |
| Budget exhausted | Stop honestly, report partial coverage with named gaps |

- 3 — every injected failure handled as above.
- 1 — some failures handled, at least one silently papered over.
- 0 / FAIL — the swarm invented content to fill a gap.

---

## Per-run verdict

Record in `evaluation.md`:

- one line per metric: score, PASS/FAIL/UNKNOWN, and the evidence line or count;
- the single highest-severity defect;
- whether the run is eligible for comparison with other runs (requires
  `benchmark.json` task id, mode, and a complete `metrics.json`).

Do not average the 13 metrics into one composite number. A run that passes the blocking
metrics (2, 4, 5, 10) and fails coverage is categorically worse than a run that passes
coverage and fails speed, and a single number would hide that.