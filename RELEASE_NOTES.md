# DEEP RESEARCH SWARM v0.1.0-beta — First Public Beta

## Highlights

- **Six-agent architecture** for LobeHub
  - Curator / Research Director (Supervisor)
  - Wide Web Scout (Discovery, query fan-out, candidate pool)
  - Primary Source Hunter (provenance-first)
  - Evidence Analyst (Evidence Ledger + Claim/Entity/Source graphs)
  - Fact Checker / Red Team (blocking Quality Gate)
  - Research Synthesizer (one final message with claim-level citations)
- **Curator-controlled orchestration** — star topology, specialists do not recursively delegate
- **Query fan-out** with `CORE / SYNONYM / TECHNICAL / OFFICIAL / NEGATIVE / CRITICISM / COMPARISON / COMMUNITY / GITHUB / RECENT / LOCAL LANGUAGE` families
- **Candidate pool → retrieval judge → progressive reranking** → deep read
- **Primary-source verification** with five-step citation verification
- **Evidence Ledger** schema (`CLAIM | TYPE | EVIDENCE | SOURCE | URL | PASSAGE | VERSION | DATE | CONFIDENCE | STATUS | VERDICT`)
- **Claim / Entity / Source graph** above the ledger
- **Red Team Quality Gate** that tries to DISPROVE the candidate answer
- **Citation audit** with five-step verification and `CITATION ENTITLEMENT` checks
- **Research modes**: ⚡ QUICK · 🔹 STANDARD · 🔎 DEEP · 🧠 MAX · 🧬 ULTRA
- **Stable sequential fallback** when the parallel orphan-call warning appears
- **EN / RU / ZH documentation** with consistent switching banner
- **LobeHub installation guide** (`docs/lobehub-installation.md`)
- **Acceptance test** (`tests/acceptance-test.md`)
- **Reproducible secret scan** (`tools/scan-secrets.py`, 0 hits at release time)

## What this is NOT

- Not a hosted service.
- Not an official LobeHub product.
- Not a single-prompt "deep research" hack.
- Not affiliated with Perplexity / OpenAI / Anthropic / LangChain / Google DeepMind / Moonshot — see `README.md` "Design inspirations / related work" for the documented patterns that informed the design.

## What's in the box

- `agents/` — 6 live system prompts exported from the live group, with per-agent role, recommended model profile, required/optional tools, and boundaries.
- `group/` — group system prompt (Markdown + raw text), routing rules, research modes, fallback policy.
- `docs/` — architecture, LobeHub installation, tools, Evidence Ledger, citation policy, quality gate, troubleshooting, known issues.
- `examples/` — 5 worked examples (QUICK, DEEP, GitHub-first, model comparison, MAX long-form).
- `tests/` — quick test, orchestration test, acceptance test, secret scan.
- `assets/` — 4 SVG diagrams (architecture, installation flow, research pipeline, quality gate).
- `tools/scan-secrets.py` — reproducible secret scanner.
- `LICENSE` (MIT) · `CHANGELOG.md` · `SECURITY.md` · `CONTRIBUTING.md` · `README.md` · `README.ru.md` · `README.zh-CN.md`.

## Notes for the maintainer

The current push to `origin` was blocked by GitHub credential constraints in this environment (the available GitHub credential is local-only; raw `git push` returns `Invalid username or token` even with a freshly-issued header). The release is fully prepared in `D:\AI\work\release\repo\`. To publish from a machine where `gh auth login` is interactive, run:

```bash
gh auth login --git-protocol https
cd /path/to/DEEP-RESEARCH-SWARM-v0.1.0-beta
git push origin main --follow-tags
gh release create v0.1.0-beta --title "DEEP RESEARCH SWARM v0.1.0-beta — First Public Beta" --notes-file RELEASE_NOTES.md
```

If interactive login is not possible, the same content is shipped as a git bundle (`DEEP-RESEARCH-SWARM-v0.1.0-beta.bundle`) and a zip archive (`DEEP-RESEARCH-SWARM-v0.1.0-beta.zip`); they can be unpacked and force-pushed.

The release is also marked `READY TO PUBLISH` in the final report.