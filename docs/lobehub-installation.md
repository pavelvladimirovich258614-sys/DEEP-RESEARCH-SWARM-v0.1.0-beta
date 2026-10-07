# Installation in LobeHub

> Audience: a person opening LobeHub for the first time. No prior knowledge of groups is required.

This guide walks through:

1. creating a new LobeHub group,
2. adding the Supervisor (Curator),
3. adding the five specialists,
4. pasting each agent's live system prompt,
5. enabling the right tools and skills,
7. configuring the group prompt and routing,
8. running the acceptance test.

## 1. Create a new Group

1. Open LobeHub.
2. Click **+ New conversation** → **Group**.
3. Title: `🔎 DEEP RESEARCH SWARM`.
4. Avatar: 🔎.
5. Background color: `#0F172A` (optional, recommended for visual distinction).
6. Description: paste from `group/group-prompt.md` (Summary section).
7. Save.

## 2. Create the Supervisor (Curator)

The Supervisor is the entry point. It is the only agent that talks to the user directly.

1. Inside the new group, click **Add agent**.
2. Title: `Curator / Research Director`.
4. **System prompt:** paste verbatim from `agents/curator.md` (the fenced block labeled `SYSTEM PROMPT`). Do not paraphrase. Do not shorten. Do not add your own preamble.
5. **Plugins / tools:** enable the following (REQUIRED):
   - `lobe-web-browsing`
   - `lobe-browser`
   - `lobe-artifacts`
   - `lobe-agent-documents`
   - `lobe-agent-management`
6. Optional: any skills relevant to your research domain (NOT random skill packs).
7. Mark as **Supervisor** in the group settings.
8. Save.

## 3. Add Wide Web Scout

1. **Add agent** in the same group.
3. Title: `🌐 Wide Web Scout`.
4. **System prompt:** paste verbatim from `agents/wide-web-scout.md`.
5. **Plugins / tools:** enable:
   - `lobe-web-browsing`
   - `lobe-browser`
   - `lobe-agent-browser`
   - `github` (optional, but recommended for GitHub queries)
   - `twitter` (optional, for X queries)
6. Save.

## 4. Add Primary Source Hunter

1. **Add agent**.
3. Title: `🏛️ Primary Source Hunter`.
4. **System prompt:** paste verbatim from `agents/primary-source-hunter.md`.
5. **Plugins / tools:** enable:
   - `lobe-web-browsing`
   - `lobe-browser`
   - `lobe-agent-browser`
   - `lobe-cloud-sandbox` (for running CLI scripts when needed)
   - `pollinations-pollinations-web-research` (optional)
   - `github`
6. Save.

## 5. Add Evidence Analyst

1. **Add agent**.
3. Title: `🧪 Evidence Analyst`.
4. **System prompt:** paste verbatim from `agents/evidence-analyst.md`.
5. **Plugins / tools:** enable:
   - `lobe-web-browsing`
   - `lobe-agent-browser`
   - `lobe-agent-documents`
   - `lobe-cloud-sandbox`
   - `lobe-artifacts`
6. Save.

## 6. Add Fact Checker / Red Team

1. **Add agent**.
3. Title: `🕵️ Fact Checker / Red Team`.
4. **System prompt:** paste verbatim from `agents/fact-checker-red-team.md`.
5. **Plugins / tools:** enable:
   - `lobe-web-browsing`
   - `lobe-browser`
   - `lobe-agent-browser`
   - `lobe-agent-documents`
   - `lobe-artifacts`
6. Save.

## 7. Add Research Synthesizer

1. **Add agent**.
3. Title: `🧠 Research Synthesizer`.
4. **System prompt:** paste verbatim from `agents/research-synthesizer.md`.
5. **Plugins / tools:** enable:
   - `lobe-agent-documents`
   - `lobe-agent-management`
   - `lobe-agent-browser`
   - `lobe-computer-use` (for very long final reports)
   - `lobe-artifacts` (optional)
6. Save.

## 8. Configure the Group system prompt

Open the group settings → **Group system prompt** field → paste verbatim from `group/group-prompt-raw.txt` (or use the Markdown-wrapped version in `group/group-prompt.md`). Do not paraphrase.

## 9. Configure research modes and routing

Routing is encoded inside the group system prompt; you do not need to configure it separately. The four companion documents in `group/` describe the rules in plain English:

- `group/group-prompt.md` — full live prompt + summary
- `group/routing-rules.md` — how workstreams are dispatched
- `group/research-modes.md` — QUICK / STANDARD / DEEP / MAX / ULTRA
- `group/fallback-policy.md` — retry, orphan-fix, Analyst DEGRADED fallback

## 10. Start a fresh conversation

Always start a **fresh conversation** when running deep research. Long histories break claim-level citations: the Synthesizer must rely on the current Evidence Ledger, not on earlier outputs.

## 11. Run the acceptance test

Before doing real research, run `tests/acceptance-test.md`. It checks:

- the Supervisor is correctly marked,
- all six agents are present with the right tools,
- the group prompt was pasted verbatim,
- a simple QUICK question returns the QUICK output format with citations,
- a simple DEEP question returns the full pipeline,
- the Fact Checker can issue a `FAIL`,
- the Synthesizer at most runs **after** `PASS`.

If any of these checks fail, fix the configuration before doing real research.

## Common pitfalls

| Symptom | Likely cause |
|---|---|
| Supervisor re-answers questions that should go to a specialist | Supervisor prompt was shortened; re-paste from `agents/curator.md` |
| Fact Checker never returns FAIL | Prompt was paraphrased and lost the "disprove" framing |
| Synthesizer writes without citations | Group prompt was paraphrased and lost the Quality Gate |
| "Orphaned skill call" warnings during parallel Scout∥Hunter | Group prompt was paraphrased and lost the SEQUENTIAL TOOL CALLS rule |
| Tools unavailable | Provider/model settings don't support the tool; switch provider or remove the tool |

See `troubleshooting.md` for more.