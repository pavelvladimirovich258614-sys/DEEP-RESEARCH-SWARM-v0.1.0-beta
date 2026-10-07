# Acceptance test

This is the **end-to-end** check you should run after configuration and before any real research. It is the closest thing to an integration test that a multi-agent prompt system can have.

## What it validates

- the configuration matches the live export (see `agents/*.md` and `group/group-prompt-raw.txt`);
- the group has the right tools and skills;
- the QUICK, STANDARD, DEEP, MAX modes all work;
- the Fact Checker can return both `PASS` and `FAIL`;
- the Synthesizer is blocked on `FAIL`;
- the orphan-fix behaves (no runtime warnings, or fallback to STABLE MODE).

## Pre-flight

```
[ ] Group name matches "🔎 DEEP RESEARCH SWARM"
[ ] Group prompt is verbatim from group/group-prompt-raw.txt
[ ] Curator is marked as Supervisor
[ ] Each agent has the matching live prompt in agents/<role>.md
[ ] Each agent has the required plugins enabled
[ ] No agent has stray plugins the protocol did not require
[ ] LobeHub version is compatible (see docs/known-issues.md)
[ ] No orphaned skill call after the configuration in recent runs
```

## Run

Start a fresh conversation. Ask each of the following, in order:

### A1 — quick fact

> What's the latest stable version of <popular open-source tool>?

Expect:

- Curator answers without delegation.
- Output matches the QUICK format.

### A2 — DEEP comparison with a contradiction

> Compare <X> and <Y> for <use case>.

Expect:

- mode auto-picks `🔎 DEEP`;
- workstreams: discovery, primary sources, analysis, fact-check, synthesis;
- Fact Checker reports its verdict with at least one SUPPORTING and one POTENTIALLY CONTRADICTING evidence;
- Final answer has a comparison table with claim-level citations.

### A3 — Fact Checker FAIL

Ask a question whose correct answer requires a fact the README does not document:

> Does <project> support platform <Z> as a first-class citizen?

Expect:

- Fact Checker returns `FAIL` with `OPEN_GAPS: Z = NOT DOCUMENTED`;
- the Synthesizer does not write the final answer;
- the Curator dispatches a targeted task and the loop continues until either the gap closes or the STOP RULE fires;
- the final answer either confirms the gap or honestly says `NOT VERIFIED`.

### A4 — MAX with target gap closure

Ask a MAX question with at least one known gap (e.g., a niche tool whose Windows install path is unclear). The final answer should:

- mention the gap explicitly,
- include the targeted search queries that were tried,
- either close the gap or mark it `NOT VERIFIED` with the closest evidence.

### A5 — orphan-fix regression

Ask a question that triggers Scout ∥ Hunter parallel discovery. Expect:

- no "orphaned skill call" warnings in the run,
- if warnings appear, switch to STABLE MODE and re-run.

## Pass criteria

- all 5 tests above produce the expected shape;
- the Research Audit section of the final answers contains MODE / WS / ROUNDS / SOURCES_OPENED / PRIMARY_SOURCES / COMMUNITY_SOURCES / GAPS_LEFT / QUALITY_GATE;
- no API keys, tokens or account identifiers appear in any agent's output;
- no `agt_xxx` or `cg_xxx` IDs from your personal LobeHub account leak into the answer.

## Fail criteria

- Synthesizer runs after Fact Checker `FAIL` → protocol violation, re-paste group prompt.
- Final answer is missing claim-level citations → protocol violation, re-paste group prompt.
- An agent's output mentions an `agt_xxx` / `cg_xxx` / `user_xxx` ID → that's a leak; sanitize before continuing.
- Tests 1 and 4 take wildly different amounts of time without an obvious reason → investigate.