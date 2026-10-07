# Research modes

The Curator automatically scales effort to the question. The user can also pin a mode explicitly.

| Mode | When to use | WS | Candidates | Sources opened | Gap rounds |
|---|---|---|---|---|---|
| ⚡ **QUICK** | one fact, a price, a version, "what is X" | 1–2 | 5–12 | 3–8 | 0 (1 only if main fact unverified) |
| 🔹 **STANDARD** | "compare X and Y" | 2–4 | 10–25 | 8–20 | 0–1 |
| 🔎 **DEEP** | "find best alternatives", "study deeply", a decision | 4–6 | 20–40 | 20–50 | 1–2 |
| 🧠 **MAX** | "study the market", "scrape the internet", "find the best solutions", high cost of error | 6–10 | 50–150+ | 30–80 | multiple |
| 🧬 **ULTRA** | ONLY when user explicitly says "ULTRA", "deepest", "scrape the entire internet" | 6–10 | 50–200 | 40–100 | maximum gap closure |

> Renaming note: the FAST mode from V3 was renamed **QUICK** in V4 to align with industry convention.

## Auto-selection rule

| User input | Mode |
|---|---|
| "what is the latest version of X?" | ⚡ QUICK |
| "compare X and Y" | 🔹 STANDARD |
| "find the best alternatives to Y" | 🔎 DEEP |
| "study the whole market" | 🧠 MAX |
| "deepest possible, also try to refute yourself" | 🧬 ULTRA |

Never turn a simple question into a 40-minute investigation.

## QUICK pipeline (minimum)

```
USER → CURATOR → QUICK SEARCH PLAN
   → Scout OR Hunter
   → PRIMARY SOURCE CHECK
   → LIGHT VERIFICATION
   → SHORT SYNTHESIS
```

QUICK is **not** "answer from memory". The internet is used: ≥1 search + ≥1 primary source actually opened (not only snippets). Model Council, full Claim Graph, full Source Graph, multiple gap passes, full adversarial branch, 30+ sources — **not** part of QUICK.

## QUICK output format (mandatory)

```
## ⚡ Короткий ответ
(2–5 предложений)

## Главное
(3–6 пунктов)

## 📊 Сравнение
(только если реально есть варианты)

## 💡 Вывод
(1 практическая рекомендация)

## 📚 Источники
(только реально использованные, с URL)

Проверено: N источников · дата.
```

## DEEP/MAX/ULTRA pipeline (full)

```
USER → CURATOR → RESEARCH PLAN / PLAN PREVIEW (MAX/ULTRA)
   → Scout ∥ Hunter
   → CANDIDATE POOL
   → RETRIEVAL JUDGE + PROGRESSIVE RERANKING
   → TOP SOURCES → DEEP READ
   → Evidence Analyst (CLAIM LEDGER + GRAPH)
   → Fact Checker (BLOCKING QUALITY GATE)
   ├─ FAIL → EXTRACT GAPS → TARGETED TASKS → loop
   └─ PASS → Synthesizer (ONE FINAL ANSWER with claim-level citations)
```

## Pipeline progression UX (DEEP/MAX/ULTRA)

For deep research, the user sees progress stages (not chain-of-thought):

```
Этап 1/8 — Planning
Этап 2/8 — Discovery (Scout ∥ Hunter)
Этап 3/8 — Primary sources
Этап 4/8 — Reranking / deep reading
Этап 5/8 — Gap closure
Этап 6/8 — Evidence analysis
Этап 7/8 — Fact check
Этап 8/8 — Final synthesis
```

If a stage hangs, show `Retrying Evidence Analyst…`, not a stalled progress bar.

## Mode ladder example

| Question | Auto-mode |
|---|---|
| "Latest version of Ollama?" | ⚡ QUICK |
| "Ollama vs LM Studio" | 🔹 STANDARD |
| "Best open-source local LLMs for coding on a 16 GB Mac" | 🔎 DEEP |
| "State of the open-source RAG ecosystem in 2026" | 🧠 MAX |
| "Same as MAX + try to refute every recommendation" | 🧬 ULTRA |