# 🔎 DEEP RESEARCH SWARM

**Search wide. Verify deep. Answer once.**

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md)

> **Status:** `v0.1.0-beta`
> A public beta configuration for LobeHub — six specialized agents coordinated by a single Curator. Not a hosted service. Not an official LobeHub product.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Release: beta](https://img.shields.io/badge/Release-beta-orange.svg)
![LobeHub](https://img.shields.io/badge/Built%20for-LobeHub-1f6feb.svg)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-blueviolet.svg)
![Deep Research](https://img.shields.io/badge/Use%20case-Deep%20Research-2e7d32.svg)

---

## Why this project exists

Most "research agents" cram several jobs into one prompt: search, source selection, reading, verification, contradiction handling, and writing. DEEP RESEARCH SWARM splits those jobs across specialized agents coordinated by a single Curator. The point is **not** to maximize the number of agents — the point is to build a disciplined evidence pipeline.

The system:

- fans out across the web, GitHub, forums, papers and official docs;
- prefers primary sources over summaries;
- keeps claims tied to provenance;
- distinguishes facts, source claims, community signals, and hypotheses;
- detects contradictions instead of smoothing them over;
- runs targeted second-pass verification when evidence is weak;
- returns **one coherent final answer with real citations**.

## Architecture

![Architecture](assets/architecture.svg)

```
User
  │
  ▼
Curator / Research Director (Supervisor)
  │
  ├──► Wide Web Scout
  │       discovery · query fan-out · candidate pool
  │
  ├──► Primary Source Hunter
  │       official docs · repos · papers · filings · release notes
  │
  ├──► Evidence Analyst
  │       deep reading · evidence ledger · claim/source graph
  │
  ├──► Fact Checker / Red Team
  │       contradiction search · citation audit · blocking quality gate
  │
  └──► Research Synthesizer
          final synthesis · uncertainty · citations · actionable answer
```

This is a **supervisor-controlled star topology**. Specialists return their work to the Curator; they do not recursively delegate to one another.

## The six agents

| Agent | Mission | Typical output |
|---|---|---|
| **Curator / Research Director** | Plans, routes, controls depth, merges evidence, owns the final answer | research plan, workstreams, final decision |
| **Wide Web Scout** | Finds the broad candidate space | ranked candidate pool + discovery map |
| **Primary Source Hunter** | Goes after official docs / repos / papers / releases | provenance-first candidate list with URLs |
| **Evidence Analyst** | Deep reads, extracts passages, builds the ledger | Evidence Ledger + Claim/Entity/Source graphs |
| **Fact Checker / Red Team** | Tries to **disprove** candidate conclusions, runs the blocking Quality Gate | PASS/FAIL with gap extraction |
| **Research Synthesizer** | Writes the one final answer | single-message Markdown report with claim-level citations |

Each agent has a live system prompt in `agents/`.

## Research modes

The Curator scales effort to the question. You can also pin a mode.

| Mode | When to use | Sources opened | Gap rounds |
|---|---|---|---|
| ⚡ QUICK | single fact / version / price | 3–8 | 0 |
| 🔹 STANDARD | "compare X and Y" | 8–20 | 0–1 |
| 🔎 DEEP | "find best alternatives" / a decision | 20–50 | 1–2 |
| 🧠 MAX | "study the market" / high cost of error | 30–80 | multiple |
| 🧬 ULTRA | only when you say "deepest possible" | 40–100 | maximum |

See [`group/research-modes.md`](group/research-modes.md).

## What you get

- **One final answer** with claim-level citations, every claim traceable to a passage.
- **A real Quality Gate.** The Fact Checker tries to disprove the answer before it ships. If it fails, the run loops until critical gaps are closed or the stop rule fires.
- **Evidence Ledger + graphs.** Every claim has provenance: source class, date, retrieval date, confidence, verdict.
- **Mode-aware depth.** Quick questions get quick answers; market studies get 30+ sources.
- **Open-source MIT.** No vendor lock-in.

## Quick start

1. **Read [`docs/installation.md`](docs/lobehub-installation.md).** It walks through creating a LobeHub group, adding the six agents, pasting each prompt, and enabling the required tools.
2. **Run [`tests/acceptance-test.md`](tests/acceptance-test.md).** This validates the configuration before any real research.
3. **Try [`examples/quick-research.md`](examples/quick-research.md)** as your first run.
4. **Try [`examples/deep-research.md`](examples/deep-research.md)** for a real pipeline.

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — why the pipeline looks the way it does
- [`docs/lobehub-installation.md`](docs/lobehub-installation.md) — step-by-step setup
- [`docs/tools-and-skills.md`](docs/tools-and-skills.md) — what each agent uses
- [`docs/evidence-ledger.md`](docs/evidence-ledger.md) — schema, confidence, claim graph
- [`docs/citation-policy.md`](docs/citation-policy.md) — five-step verification
- [`docs/quality-gate.md`](docs/quality-gate.md) — the blocking gate
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — common failure modes
- [`docs/known-issues.md`](docs/known-issues.md) — what the system does **not** claim

## Examples

- [`examples/quick-research.md`](examples/quick-research.md) — QUICK pipeline example
- [`examples/deep-research.md`](examples/deep-research.md) — DEEP pipeline example
- [`examples/github-research.md`](examples/github-research.md) — provenance-first
- [`examples/model-comparison.md`](examples/model-comparison.md) — adversarial + benchmark normalization
- [`examples/long-form-technical-research.md`](examples/long-form-technical-research.md) — MAX with target gap closure

## Repository layout

```
DEEP-RESEARCH-SWARM-v0.1.0-beta/
├── README.md             ← this file (EN)
├── README.ru.md           ← Russian translation
├── README.zh-CN.md       ← Chinese (Simplified) translation
├── LICENSE               ← MIT
├── CHANGELOG.md
├── SECURITY.md
├── CONTRIBUTING.md
├── agents/               ← live system prompts for the six agents
├── group/                ← group prompt, routing, modes, fallback
├── docs/                 ← deep documentation
├── tests/                 ← acceptance + orchestration + secret scan
├── examples/             ← worked examples (5)
```

## Design inspirations / related work

DEEP RESEARCH SWARM draws on documented patterns from:

- Perplexity Deep Research
- OpenAI Deep Research
- Gemini Deep Research
- Kimi Researcher
- GPT Researcher
- DeerFlow
- LangChain Open Deep Research
- Anthropic multi-agent research (orchestrator-worker, four-field delegation contract, effort scaling, LLM-judge rubric)

This repository does **not** include any proprietary prompts from the above systems. It is not affiliated with, endorsed by, or supported by any of those organizations. Names are used solely to acknowledge the documented architectural patterns that informed the design.

## License

MIT — see [`LICENSE`](LICENSE).