# Agent prompt analysis

Baseline analysis of the six live prompts and the group prompt, done **before** any
benchmark run. Purpose: record what each agent is currently specified to do, where the
specifications overlap, and which risks are visible from the text itself.

This document deliberately makes **no prompt changes**. Per the project principle
(`MEASURE → FIND FAILURE → FIX → RETEST`), every recommendation below is a hypothesis to
be tested against `tests/research-benchmark/`, not a fix to apply now.

## How this was derived

Read directly from the tracked files:

- `agents/curator.md` — 321 lines, 35.8 KB
- `agents/research-synthesizer.md` — 312 lines, 29.1 KB
- `agents/fact-checker-red-team.md` — 271 lines, 24.5 KB
- `agents/primary-source-hunter.md` — 270 lines, 21.9 KB
- `agents/evidence-analyst.md` — 266 lines, 22.1 KB
- `agents/wide-web-scout.md` — 236 lines, 21.0 KB
- `group/group-prompt-raw.txt` — 450 lines, 54.1 KB, sections 0–72

Claims are labelled **[observed]** when read from the files and **[hypothesis]** when
inferred and still in need of a run to confirm.

---

## Cross-cutting findings

### X1. The specification accreted in layers and was never consolidated — [observed]

Every prompt is layered `V2 → V3 → V3.1 → V4 → V4.1`, with earlier layers marked
"fully preserved". The group prompt carries this literally in its title and section list
(`## 1–22. ЯДРО V2 (ПОЛНОСТЬЮ СОХРАНЕНО)`).

Risk: where a later section tightens or changes an earlier rule, the model receives both
and must resolve the conflict at runtime. There is no consolidated, single-source rule
set. This is a plausible contributor to inconsistent behaviour, and it is measurable:
if two layers disagree, the same query run twice should sometimes produce different
answers.

Note in fairness: the V2 core is **not** lost. In the group prompt it is compressed into
dense bullet rules rather than dropped, which was verified by reading lines 24–50. The
issue is layering and conflict, not truncation.

### X2. The Curator prompt is the largest and the most patched — [observed]

`curator.md` is 321 lines / 35.8 KB and carries the densest hardening stack: twelve V4
subsections (A–L) plus a V4.1 hotfix, on top of V3.1 dispatch rules. It is simultaneously
the planner, the mode selector, the dispatcher, the gap-budget owner and the owner of the
QUICK solo path.

**[hypothesis]** The largest risk of instruction dilution sits in the agent that has the
least room to discard instructions, because every one of its rules is load-bearing for
coordination.

### X3. Substantial rule duplication across agents — [observed]

Rule blocks present in more than one agent prompt, counted mechanically:

| Rule block | Appears in |
|---|---|
| WINDOWS / support-block contract | curator, analyst, checker, hunter, synthesizer, scout (all 6) |
| PROMPT-INJECTION SHIELD | all 6 |
| ORPHAN-FIX tool-call hygiene | curator, analyst, checker, hunter, scout (5) |
| QUERY FAN-OUT | curator, hunter, scout (3) |
| BENCHMARK CLAIMS | checker, hunter, scout (3) |
| VERSION AWARENESS | analyst, hunter, scout (3) |
| NEGATIVE CLAIM RULE | analyst, checker, hunter (3) |
| GITHUB FIELD SEMANTICS | analyst, checker, hunter (3) |
| SOURCE PROVENANCE GRAPH | analyst, hunter |
| CANDIDATE POOL | curator, hunter, scout |
| RETRIEVAL JUDGE | curator, analyst |
| MODEL COUNCIL | curator, checker |

Some duplication is correct and intentional: the group prompt defines a single
consequence chain, and a defensive rule repeated in the agent that must enforce it is
reasonable. The finding is that duplication is **unbounded** — there is no stated rule
about which agent owns which contract, so "the Hunter enforces X" and "the Analyst
enforces X" are both true readings.

**[hypothesis]** Overlapping enforcement is the most likely mechanical cause of
metric 7 (AGENT SPECIALIZATION) and metric 8 (DUPLICATION) failing: when three agents
carry the same rule, they can produce the same artefact for the same reason.

### X4. Model recommendations are inconsistent across the six agents — [observed]

| Agent | Recommended model |
|---|---|
| Curator | Mistral Large 4 |
| Evidence Analyst | MiniMax-M3 |
| Fact Checker | MiniMax-M3 |
| Primary Source Hunter | MiniMax-M3 |
| Wide Web Scout | Qwen3.8-flash |
| Research Synthesizer | Qwen3.8-flash |

Two flags, kept separate because they have different certainty:

- **`Qwen3.8-flash` needs verification.** It is written the same way as the other model
  names, but I could not confirm such a model exists. Do not treat this as a typo claim —
  check it against the model list actually available in the installation. If it is
  wrong, Scout and Synthesizer were configured with an unresolvable recommendation.
- **Practical availability.** The recommended set spans three vendors. If the deployment
  has access to only one of them, four of six recommendations are inert, and the roles
  that matter most for verification (Hunter, Checker) may be running on a fallback model
  rather than the intended one.

### X5. QUICK mode bypasses the swarm entirely — [observed]

`curator.md` V4.1 "HF-1. QUICK SOLO EXECUTION" directs the Curator to answer alone
without delegation. This is a sensible latency optimisation, but it means **a QUICK run
cannot produce evidence about specialization or duplication** — there is one agent.

Consequence for benchmarking: metrics 7 and 8 are only meaningful for STANDARD and
above. All 15 benchmark tasks expect DEEP or higher, which is correct and should be
enforced during runs.

---

## Agent-by-agent

### AGENT 1 — Curator / Supervisor / Research Director

- **Role [observed]:** sole coordinator. Chooses mode, compiles the SEARCH_PROGRAM,
  dispatches Scout/Hunter in parallel, owns gap budgets and the STOP RULE, owns the
  anti-orphan dispatch rules. The group prompt explicitly states nobody else answers the
  user directly and nobody else decides who goes next.
- **Strength [observed]:** the most complete coverage of orchestration mechanics of the
  six. It owns failure paths — timeout/retry, analyst degraded fallback, duplicate
  dispatch labelling, targeted gap search — rather than delegating failure handling
  downstream.
- **Weakness [hypothesis]:** X2 above — largest prompt, densest patching. Additionally,
  it owns both "decide the mode" and "execute QUICK solo", so a mode misclassification
  silently degrades a multi-agent run into a single-agent run with no visible error.
- **Overlap:** QUERY FAN-OUT, CANDIDATE POOL, RETRIEVAL JUDGE, MODEL COUNCIL, WINDOWS
  block — all duplicated with Scout/Hunter/Analyst/Checker (X3).
- **Recommended change (test first):** do not add or remove rules. Instead, measure whether
  mode selection is correct across the 15 benchmark tasks. If mode is often wrong, the
  fix is to the mode ladder's decision inputs, not to the prompt's bulk.

### AGENT 2 — Wide Web Scout (Discovery)

- **Role [observed]:** breadth-first discovery. Query fan-out, hybrid retrieval,
  search-diversity guard, candidate pool, mode-aware saturation. Explicitly discovery —
  it is meant to be the agent that finds *more* places to look, not the one that verifies.
- **Strength [observed]:** the clearest separation of discovery from verification of any
  agent, and it carries search-diversity and saturation logic that no other agent owns.
- **Weakness [hypothesis]:** carries VERSION AWARENESS, BENCHMARK CLAIMS and
  CANDIDATE POOL rules that belong to Hunter and Analyst. A discovery agent that applies
  verification rules starts doing Hunter's work, which is exactly the
  metric 7 failure mode.
- **Overlap:** highest of the six — QUERY FAN-OUT, CANDIDATE POOL and VERSION AWARENESS
  are all also in Curator/Hunter.
- **Recommended change (test first):** score Scout output for whether it stays
  discovery-shaped. If Scout outputs verified verdicts, the contract boundary needs
  sharpening; if it stays discovery-shaped, leave it alone.

### AGENT 3 — Primary Source Hunter

- **Role [observed]:** provenance-first retrieval — official docs, repos, releases,
  issues, papers, filings, standards. Carries the categorical-claim validation blocks,
  version scope, repository health, Windows support contract, and absence-of-evidence.
- **Strength [observed]:** the most detailed contract for *how a source is judged*, and
  the only agent carrying the repository-health and Windows-support blocks. This is the
  strongest anti-hallucination surface in the system.
- **Weakness [hypothesis]:** the ruleset is the widest of the six after the Curator and
  is split across V2/V3/V4 subsections, which raises the chance that a rule exists but is
  never applied in practice. Also shares GITHUB FIELD SEMANTICS with two other agents.
- **Overlap:** BENCHMARK CLAIMS with Scout and Checker; GITHUB FIELD SEMANTICS with
  Analyst and Checker; SOURCE PROVENANCE GRAPH with Analyst.
- **Recommended change (test first):** BR-03 and BR-13 target this agent directly. If
  primary-source counts are low relative to the citation quality score, the Hunter is
  underperforming and its scope needs widening, not re-specification.

### AGENT 4 — Evidence Analyst

- **Role [observed]:** constructs the Evidence Ledger plus the claim, entity and source
  graphs. Owns the FACT / SOURCE CLAIM / INTERPRETATION / INFERENCE / UNKNOWN typing,
  confidence assignment, and reduced-scope chunked execution for long inputs.
- **Strength [observed]:** the only agent whose output is a structured artefact rather
  than prose. The claim-type taxonomy is the system's main defence against a confident
  interpretation being recorded as a fact, and degraded-mode chunking shows real
  attention to context limits.
- **Weakness [hypothesis]:** runs **after** discovery and Hunter, so it inherits their
  quality. If upstream evidence is thin, ledger construction faithfully records a thin
  evidence base — which is correct behaviour but will look like an Analyst failure in a
  naive reading. Score it only in combination with upstream metrics.
- **Overlap:** shares NEGATIVE CLAIM RULE with Checker and Hunter, VERSION AWARENESS
  with Hunter and Scout, SOURCE PROVENANCE GRAPH with Hunter.
- **Recommended change (test first):** no change proposed. This agent is the most
  structurally sound of the six. Verify that ledger rows carry passage-level evidence
  rather than just URLs before considering anything.

### AGENT 5 — Fact Checker / Red Team

- **Role [observed]:** disconfirmation. Temporal validation, categorical-claim checks,
  community-to-fact promotion rules, confidence audit, citation verification chain,
  citation coverage and entitlement, negative evidence, claim-graph cascade. Owns the
  **blocking** quality gate: on FAIL the Synthesizer is prohibited from running.
- **Strength [observed]:** the only component with veto authority, and it is the only one
  that checks the system's own output rather than the world. The negative-claim and
  snippet rules are the specific defences against the two most common failure modes
  (absence-of-evidence assertions, and snippet treated as proof).
- **Weakness [hypothesis]:** a gate that blocks must be applied reliably. If it FAILs
  spuriously the swarm stalls; if it passes a weak evidence package the entire architecture
  is decorative. The gate's failure rate in both directions is the single most valuable
  number the benchmark can produce.
- **Overlap:** MODEL COUNCIL with Curator; NEGATIVE CLAIM and GITHUB FIELD SEMANTICS with
  Hunter; WINDOWS block with all agents.
- **Recommended change (test first):** instrument gate verdicts across all 15 tasks.
  If FAIL is essentially never returned, the blocking behaviour is nominal rather than
  real, and the honest conclusion is that the Synthesizer is running ungated.

### AGENT 6 — Research Synthesizer

- **Role [observed]:** the only agent that writes the user-facing answer. Owns content
  preservation, abstention, one-final-report discipline, one-click copy, presentation
  layer, self-evaluation, and citation fidelity.
- **Strength [observed]:** carries the strongest anti-drift guard of the six — content
  preservation, explicitly forbidden from introducing new facts during synthesis, and a
  citation-fidelity section.
- **Weakness [hypothesis]:** its output-standard block appears **repeated** within the
  prompt, in the V3 section and again in the V4 section. Repetition of a long template
  is a known way to produce inconsistent formatting and to consume budget without adding
  constraints. This is the one structural observation here worth checking first, and it
  is verifiable by counting blocks, not by running a benchmark.
- **Overlap:** lowest of the six — this is the one agent with a genuinely distinct job.
  It shares only the WINDOWS block and the injection shield, both of which are inherited
  safety rules rather than role overlap.
- **Recommended change (test first):** metrics 5 and 10 are the tests. If
  `urls_in_final_not_in_agents` is non-zero, synthesis is inventing citations, which is
  the failure its own fidelity section is written to prevent.

---

## Group prompt (`group/group-prompt-raw.txt`)

450 lines, 54.1 KB, 72 numbered sections spanning V2 (0–22), V3 (23–60), V3.1 (57–59)
and V4 (61–72). Verified by reading lines 1–56 and extracting the section list.

Against the five questions asked of it:

| Question | Finding |
|---|---|
| Does it lose evidence? | **No, not by truncation.** The V2 core survives as compressed bullet rules (lines 26–49), including the ledger schema, confidence definitions and the citation verification chain. Risk is conflict between layers, not loss. |
| Does it mix fact and assumption? | **It explicitly forbids it.** Claim types are enumerated at line 34 (`FACT / SOURCE CLAIM / INTERPRETATION / INFERENCE / COMMUNITY EXPERIENCE`), with the instruction not to mix them. Whether agents obey is an empirical question for metric 4. |
| Can it resolve contradictions? | **It requires it, twice.** New Candidate Validation (line 32) and the Red Team gate (line 44) both force a contradiction into the open. Resolution *quality* is untested — BR-10 is built to probe exactly this. |
| Does it preserve citations? | **Yes, and it goes further than preservation.** Lines 43 and 264 define a six-step citation verification chain and a Citation Entitlement check, where a citation that does not entail its claim is a failure. |
| Does it create new facts at synthesis? | **Forbidden explicitly.** Line 46 states the Synthesizer uses only verified material and may not invent; if no fact exists the output must be `UNKNOWN` / `NOT VERIFIED`. |

**Verdict on the group prompt:** it is coherent and unusually explicit about the failure
modes it wants to prevent. Its weakness is not content but **volume and layering** — 72
sections accumulated across four versions with no consolidation, and the same rules
restated in each agent (X3).

---

## The most important open question

The architecture is built around a blocking quality gate (Fact Checker → PASS/FAIL →
Synthesizer). Everything else in the system exists to feed that gate.

Therefore the first number to obtain is not a quality score. It is:

> **Across 15 benchmark runs, how many times did the Fact Checker return FAIL, and what
> happened to each one?**

If the answer is zero, the gate is decorative, every downstream quality metric is
measured on ungated output, and the most useful benchmark finding is that the system
needs its gate made real. If the answer is non-zero, the interesting question becomes
whether each FAIL was correct and whether the targeted gap-closure loop recovered from
it.

Either result is worth more than any prompt rewrite, and neither can be obtained without
running the benchmark.