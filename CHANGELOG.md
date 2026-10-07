# Changelog

All notable changes to DEEP RESEARCH SWARM will be documented here.

## [v0.1.0-beta] — 2026-10-07

First public beta release.

### Added

- Six-agent architecture for LobeHub:
  - Curator / Research Director (Supervisor)
  - Wide Web Scout (Discovery)
  - Primary Source Hunter (Provenance)
  - Evidence Analyst (Ledger + Graphs)
  - Fact Checker / Red Team (blocking Quality Gate)
  - Research Synthesizer (final answer)
- Research mode ladder: ⚡ QUICK · 🔹 STANDARD · 🔎 DEEP · 🧠 MAX · 🧬 ULTRA
- Mandatory blocking Quality Gate
- Evidence Ledger + Claim / Entity / Source graphs
- Hybrid retrieval strategy (lexical + semantic)
- Search saturation and gap-budget rules
- Stable sequential fallback for unreliable parallel runs
- Analyst DEGRADED fallback (no Supervisor impersonation)
- GitHub data semantics: `pushed_at` → `LAST_PUSH`, `LAST_COMMIT` only from commits API
- Negative-claim rule and absence-of-evidence semantics
- LobeHub installation guide
- Documentation in EN / RU / ZH (3 README translations)
- Acceptance test in `tests/acceptance-test.md`
- Secret scan in `tests/secret-scan.md`
- 4 SVG diagrams: architecture, installation flow, research pipeline, quality gate
- 5 worked examples in `examples/`

### Known issues

- See [`docs/known-issues.md`](docs/known-issues.md).

### Design inspirations / related work

DEEP RESEARCH SWARM draws on documented patterns from:

- Perplexity Deep Research
- OpenAI Deep Research
- Gemini Deep Research
- Kimi Researcher
- GPT Researcher
- DeerFlow
- LangChain Open Deep Research
- Anthropic multi-agent research (orchestrator-worker, four-field delegation contract, effort scaling, LLM-judge rubric)

This repository does **not** include any proprietary prompts from the above systems and is not affiliated with, endorsed by, or supported by any of those organizations. Names are used solely to acknowledge the documented architectural patterns that informed the design.

### License

MIT — see [`LICENSE`](LICENSE).