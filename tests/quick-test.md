# Quick test

Run this **first** in your freshly configured group. It validates the basics in under two minutes.

## Setup checklist

```
[ ] group "🔎 DEEP RESEARCH SWARM" created
[ ] Curator marked as Supervisor
[ ] Six agents exist with the names from agents/*.md
[ ] Each agent has its live system prompt pasted verbatim
[ ] Required plugins per agent (see docs/tools-and-skills.md)
[ ] Group system-prompt is the live content of group/group-prompt-raw.txt
[ ] Conversation started fresh
```

## Test 1 — single fact

Ask:

> What is the current stable version of <some popular open-source tool>?

Expected:

- the Curator responds without delegating to a specialist (QUICK is solo);
- the answer follows the QUICK output format:
  ```
  ## ⚡ Короткий ответ
  ## Главное
  ## 💡 Вывод
  ## 📚 Источники
  Проверено: N источников · <date>
  ```
- there is at least one primary-source URL that you can click.

## Test 2 — clarification

Ask:

> Help me choose between X and Y for <vague need>.

Expected:

- the Curator asks **1–3** clarifying questions, not 10;
- the answer is conversational, not a final report.

## Test 3 — mode switch

Ask:

> I need the deepest possible research on <topic>. Refute them too.

Expected:
- the Curator auto-picks `🧬 ULTRA` and shows a Plan Preview before dispatching;
- the run produces a full pipeline (Scout ∥ Hunter → Analyst → Fact Checker → Synthesizer).

If Test 1 returns a marketing-style paragraph with no sources, re-paste the Curator prompt. If Test 3 dispatches without Plan Preview, re-paste the group prompt.

See [`troubleshooting.md`](../docs/troubleshooting.md) for more.