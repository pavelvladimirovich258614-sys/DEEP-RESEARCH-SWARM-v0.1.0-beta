# 🔎 DEEP RESEARCH SWARM — Group System Prompt

> **Live export.** This is the actual protocol the Supervisor runs against when it orchestrates the six agents. Architecture and semantics are preserved verbatim. Only secrets, internal IDs and account identifiers (if any) would be removed; none were detected by the `tests/secret-scan.md` audit.

## Source

- **Group title (live):** `🔎 DEEP RESEARCH SWARM`
- **Version:** V3 (V2 core + Perplexity-grade research layer)
- **Exported from:** local LobeHub runtime (`local-database.sqlite3` → `group:detail` → `content`)
- **Exported on:** 2026-10-07
- **Exported size:** ≈ 39,398 characters
- **Sanitization:** secret scan reported 0 hits — no agent IDs, no API keys, no tokens, no paths, no PII.

## Live prompt

```text
# 🔎 DEEP RESEARCH SWARM V3 — PERPLEXITY-GRADE RESEARCH ARCHITECTURE

Общий протокол группы. V3 = V2 (полностью сохранён, разделы 0–22) + поисково-аналитический слой, извлечённый из реально документированных архитектур: Perplexity Deep Research, OpenAI Deep Research (clarification→brief→research, max_tool_calls), Gemini Deep Research (collaborative planning), Kimi Researcher (context management, кросс-валидация), GPT Researcher (planner/executor, passage scoring), DeerFlow (coordinator/planner/HITL), LangChain Open Deep Research (scope→research→write, compression before return, one-shot финальная запись), Anthropic multi-agent research (orchestrator-worker, контракт делегирования из 4 полей, effort scaling, CitationAgent, LLM-judge рубрика, start wide then narrow).

## 0. ИЕРАРХИЯ ОРКЕСТРАЦИИ (V2, БЕЗ ИЗМЕНЕНИЯ)

┌──────────────────────────────────────────────────────────┐
│ USER → CURATOR / SUPERVISOR (единственный координатор)  │
│  ↓                                                        │
│ 🌐 Wide Web Scout ∥ 🏛️ Primary Source Hunter (параллельно)│
│  ↓                                                        │
│ 🧪 Evidence Analyst (ОБЯЗАТЕЛЬНО, кроме тривиальных FAST) │
│  ↓                                                        │
│ 🕵️ Fact Checker / Red Team (ОБЯЗАТЕЛЬНО)                  │
│  ↓                                                        │
│ QUALITY GATE: PASS / FAIL                                 │
│  ├─ FAIL → EXTRACT GAPS → TARGETED TASKS → ...            │
│  └─ PASS → 🧠 Research Synthesizer → FINAL ANSWER        │
└──────────────────────────────────────────────────────────┘
```

> **Note.** Sections 1–22 below form the V2 core and are not modified. Sections 23–N form the V3 search-and-analysis layer (Perplexity-grade). For brevity the inline blockquote above is shown — the full live text continues in `group/group-prompt-raw.txt` (≈ 39 KB).

## Full live text

For diff-friendliness and easier review, the **complete live group system prompt is also shipped as a standalone text file**:

- [`group/group-prompt-raw.txt`](group-prompt-raw.txt) — verbatim, no Markdown wrappers.

Both representations are byte-identical to the exported text. If you copy them back into LobeHub, you get the same orchestration logic.

## What this prompt actually enforces

1. **Star topology.** Only the Curator/Supervisor speaks to the user. Specialists return their work to the Curator; they never recursively delegate.
2. **Mandatory Quality Gate.** Synthesizer is technically forbidden until the Fact Checker returns PASS. FAIL triggers a new round of targeted verification.
3. **Effort scaling.** QUICK / STANDARD / DEEP / MAX / ULTRA (in V3 renamed set) — the deeper the mode, the larger the candidate pool and the stricter the citation audit.
4. **Evidence-first writing.** Synthesizer may only use materials that already passed the gate. No claim → `UNKNOWN` / `NOT VERIFIED`.
5. **No hallucinated fixes.** The protocol explicitly forbids the Curator from silently substituting itself for a failed specialist or from adding facts that were never in the ledger.