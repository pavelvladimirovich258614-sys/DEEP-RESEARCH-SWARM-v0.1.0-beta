# Example 2 — Deep research

> Mode: 🔎 DEEP

## User query

> I'm running an 8 GB-RAM VPS. I want to host a local RAG service that can ingest PDF / DOCX / EPUB, supports Russian and English, has an MCP server for my AI assistant, and never sends data to the cloud. Find the best architectures and pick a primary recommendation.

## What happens

1. **Curator** auto-picks `🔎 DEEP`. Four-to-six workstreams.
2. **Plan Preview** (5–8 lines, optional — only if user asked for confirmation; otherwise skipped).
3. **Wide Web Scout** + **Primary Source Hunter** in parallel.
4. Workstreams split by topic:
   - Doc → MD converters (CPU-friendly, RU + EN)
   - Lightweight RAG / Knowledge base systems
   - MCP server support
   - VPS / Docker / bare-metal constraints
5. **Candidate pool** formed (typically 20–40 sources), reranked by relevance / authority / freshness.
6. **Evidence Analyst** deep-reads the top set and the **Claim / Entity / Source graphs** are populated.
7. **Fact Checker** audits every critical claim: native Windows? ≥16 GB RAM requirement? Windows native or Docker only? MCP server native or proxy? Skill forge review confirms README links.
9. **Hypothesis** is upgraded or dropped.
11. **Synthesizer** writes the one final answer.

## Expected output shape

```
# 🔎 Local RAG on 8 GB VPS (PDF / DOCX / EPUB, RU + EN, MCP)
Исследовано: 30 кандидатов · 24 источника · 2026-10-07

## 🎯 Короткий ответ
...

## 🏆 Главные находки
...

## 📊 Сравнение
| System | RAM | Vectors | MCP | License | RU | Notes |
|---|---|---|---|---|---|---|

## 🥇 Лучшие варианты
- BEST LOCAL: ...
- BEST EASY SETUP: ...
- BEST RU+EN: ...
- BEST PRIVACY: ...

## 🔬 Подробный разбор
...

## ⚠️ Ограничения и противоречия
...

## 💡 Рекомендация
...

## 📚 Источники
- https://github.com/...
- https://docs..../
- https://arxiv.org/abs/...

## 🧾 Research Audit
MODE: DEEP · WS: 5 · ROUNDS: 2 · SOURCES_OPENED: 24 · PRIMARY_SOURCES: 17 · COMMUNITY_SOURCES: 7 · GAPS_LEFT: 2 NOT VERIFIED · QUALITY_GATE: PASS
```

## Common pitfalls in this example

- **Do not collapse "local app" into "local LLM".** A user-facing RAG tool can run locally as a Node/Python process while talking to a remote LLM. The comparison must list `APP_HOSTING`, `LLM_INFERENCE`, `SEARCH_BACKEND`, `DATA_STORAGE` separately.
- **Do not claim native Windows unless you opened the README.** Absence-of-evidence is `NOT DOCUMENTED`, not `NO`.
- **Do not rank self-reported benchmarks.** Note `SELF-REPORTED BENCHMARK` and `BENCHMARK NOT COMPARABLE` if methodology was hidden.
- **Treat community reports as community signals**, not as facts. If you cite it, point to it.

## When the Fact Checker should FAIL this run

- a citation URL doesn't open,
- a "native Windows" claim is based on a Docker-only README,
- a RAM figure is from a benchmark whose dataset and methodology aren't disclosed,
- a benchmark comparison ranks models on different datasets.