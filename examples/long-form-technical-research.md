# Example 5 — Long-form technical research

> Mode: 🧠 MAX (or 🧬 ULTRA if the user explicitly says "deepest")

## User query

> Research the state of open-source document-to-Markdown pipelines in 2026. I need 4–6 candidates that support PDF + DOCX + scanned PDFs + EPUB, run on CPU, support Russian and English, and keep working on a small VPS.

## Why MAX (not DEEP)?

- Multiple sub-axes (formats × languages × platform × accuracy).
- The user wants a comparison + ranking + Pareto-optimal shortlist.
- The decision is medium-to-high impact (production pipeline choice).
- The expected number of open sources is 30+.

## Workstream plan

```
WS1 — Discovery (Scout)
  - broad search for "PDF to Markdown 2026", "DOCX to Markdown",
    "OCR Markdown pipeline", "Russian OCR Markdown"
WS2 — Primary sources (Hunter)
  - GitHub README + LICENSE + latest release for each candidate
  - independent benchmarks / arXiv / evaluation tables
WS3 — Russian + English coverage (Hunter)
  - language support tables, OCR engines, Tesseract language packs
WS4 — VPS / CPU / RAM profile (Hunter)
  - issues tagged memory/oom, minimum RAM notes, Docker images
WS5 — Comparison with analyst models (Model Council on demand)
WS6 — Adversarial branch on the top pick (Fact Checker tries to DISPROVE)
```

## Pipeline shape

1. Round 1: discover + primary + analyst (ledger + graphs).
2. Round 2: gap closure (e.g., `mosaic-native Windows unclear` → `mosaic Windows install`, `mosaic release exe`, `mosaic Windows issue`).
3. Fact Checker audit: 5-step citation verification per row.
4. If FAIL → loop. If PASS → Synthesizer.

## Adversarial branch example

For the top pick, Fact Checker is told:

> "Assume the recommendation is WRONG. Find the strongest evidence against it."

The branch produces a "things that could go wrong with this pick" paragraph in the final answer (e.g., "this benchmark was self-reported; on Russian scanned PDFs this model underperforms compared to X; there is no community support yet").

## What the final answer contains

```
# 🔎 Document → Markdown pipelines (2026)
Исследовано: 60 кандидатов · 38 источников · 2026-10-07

## 🎯 Короткий ответ
Для CPU-only VPS с RU + EN поддержкой и форматами PDF / DOCX / scanned /
EPUB — лучший вариант: <TOP>. Альтернативы: ...

## 🏆 Главные находки
- Doc → MD конвертеры: 12 проверено, GitHub API + README
- Lightweight RAG: 23 проверено
- Embeddings: 6 кандидатов
- Cross-validator: 4 независимых источника

## 📊 Сравнение
| System | License | RU | PDF | Scanned | DOCX | EPUB | CPU | RAM | MCP | Source |

## 🥇 Лучшие варианты
- BEST QUALITY: ...
- BEST LIGHTWEIGHT: ...
- BEST RU+EN: ...
- BEST LOCAL: ...

## 🔬 Подробный разбор
...

## ⚠️ Ограничения и противоречия
- Самосообщённые бенчмарки: <N> моделей отмечены SELF-REPORTED
- Один крупный игрок заявляет "только наше API поддерживает
  Document Q&A" — это противоречит независимым тестам

## 💡 Рекомендация
...

## 📚 Источники
- 38 URL, primary 24, community 14

## 🧾 Research Audit
MODE: MAX · WS: 6 · ROUNDS: 2 · SOURCES_OPENED: 38 · PRIMARY_SOURCES: 24 ·
COMMUNITY_SOURCES: 14 · GAPS_LEFT: 1 NOT VERIFIED (Windows native for 1
candidate) · QUALITY_GATE: PASS
```

## Key invariants

- **One final message.** No drift, no workstream-by-workstream dump.
- **Single canonical text.** The Markdown-rendered and the Copy-friendly views come from one source.
- **Research Audit at the end.** MODE · WS · ROUNDS · SOURCES_OPENED · PRIMARY_SOURCES · COMMUNITY_SOURCES · GAPS_LEFT · QUALITY_GATE.
- **NOT VERIFIED is allowed.** A gap that would take 20 more minutes to close and doesn't change the recommendation is left as `NOT VERIFIED` with the closest source.