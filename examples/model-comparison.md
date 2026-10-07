# Example 4 — Model comparison

> Mode: 🔎 DEEP (or 🧠 MAX if the user explicitly says "comparing N models for serious selection")

## User query

> I need to pick between MiniMax, Qwen, and Mistral for our agent workflows. We use tool calling heavily, want a long context, and care about cost. Don't give me marketing.

## Why this is a hard case for benchmarks

- Each model is described by **itself** in the strongest light.
- Headline numbers (`95.7%`, `#1`, `beats Rival X`) rarely share a dataset, a prompt format, an evaluation metric, or a model class.
- "Best in class" with a link to the author's own chart is `SELF-REPORTED BENCHMARK` until proven otherwise.

## What the Hunter fetches

- Each model's official model card on its provider page.
- Each model's public release notes for the most recent version.
- Each model's pricing page.
- Independent tests where available (e.g., a neutral third-party arena or a published paper).
- Independent comparisons that disclose methodology, dataset, date, model class.

## What the Analyst extracts

For each model, passages covering:

- tool-calling capability (function calling spec, MCP support, JSON schema reliability),
- context window,
- cost per 1k input tokens / 1k output tokens,
- licensing terms,
- known operational quirks (rate limits, region locks, batch discounts).

## What the Fact Checker normalizes

Before any ranking, the Banner must answer:

- one task?
- one dataset?
- same conditions?
- same evaluation metric?
- comparable model class?

If `no` on any of those, the comparison is `BENCHMARK NOT COMPARABLE`. Direct ranking is forbidden.

## What the Synthesizer produces

A final answer with:

1. A short table that separates `tool calling`, `context`, `cost`, `license`, `operations` — never a single composite score.
2. A recommendation matrix keyed to user criteria (cost-sensitive / privacy / agent-first / free / low-vram).
3. A clear `SELF-REPORTED BENCHMARK` marker on every claim that came from the model author.
4. An explicit `NOT VERIFIED` on every claim that couldn't be reproduced or normalized.

## Example structure of the final answer

```
# 🔎 MiniMax vs Qwen vs Mistral for agent workflows
Исследовано: 18 кандидатов · 13 источников · 2026-10-07

## 🎯 Короткий ответ
Зависит от вашего приоритета. Если tool-calling reliability критичнее всего — ...
Если cost-per-1k — ... Если длинный контекст — ...

## 📊 Сравнение
| Criterion | MiniMax-M3 | Qwen3.8-flash | Mistral Large 4 | Source class |
|---|---|---|---|---|
| Tool calling | ... | ... | ... | docs / community |
| Context window | ... | ... | ... | docs |
| Cost / 1k in | ... | ... | ... | docs |
| Cost / 1k out | ... | ... | ... | docs |
| MCP support | ... | ... | ... | docs |
| License | ... | ... | ... | LICENSE file |
| Independent benchmark | ... | ... | ... | arena / paper |

## ⚠️ Ограничения
- Все три компании публикуют `SELF-REPORTED BENCHMARK`. Прямое сравнение
  запрещено до нормализации: BENCHMARK NOT COMPARABLE.
- Headline-номера (`95.7%`, `#1`) — не доказательство. Источник не указан
  в ряде случаев.

## 💡 Рекомендация
- BEST TOOL-CALLING: ...
- BEST COST: ...
- BEST LONG-CONTEXT: ...

## 🧾 Research Audit
MODE: DEEP · WS: 4 · ROUNDS: 1 · PRIMARY_SOURCES: 8 · COMMUNITY_SOURCES: 5 ·
GAPS_LEFT: 1 NOT VERIFIED (independent benchmark) · QUALITY_GATE: PASS
```