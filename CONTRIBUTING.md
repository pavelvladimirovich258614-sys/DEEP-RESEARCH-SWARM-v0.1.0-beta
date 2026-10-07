# Contributing

Thanks for your interest in DEEP RESEARCH SWARM.

## Scope of this repository

This repository ships a six-agent configuration for LobeHub and the documentation around it. It does **not** ship any runtime code. The "code" of this project is the live system prompts and the group prompt.

## What you can contribute

- New **examples** in `examples/` — query + expected mode + expected output shape.
- **Documentation** improvements, especially diagrams, screenshots of real runs, and worked examples.
- New **tests** in `tests/` — both the existing acceptance test and additional adversarial cases.
- **Troubleshooting** entries — what broke and how you fixed it.
- New **research modes** if you have a clear rationale, with the triggers and the pipeline shape.
- A new **agent** role if you can show that the existing six cannot cover it.

## What you should NOT contribute

- Changes that **break the evidence-first architecture**. If a contribution removes or weakens the Quality Gate, the citation verification, the `NO DUPLICATE DISPATCH` rule, or the `SEQUENTIAL TOOL CALLS` rule, it will be rejected unless you provide a compelling reason and a replacement.
- Changes that **change the live group configuration** (model, provider, tool set, plugin set) without an accompanying `tests/acceptance-test.md` re-run.
- Pull requests that contain **API keys, tokens, account IDs, or PII** — they will be closed without review and the commit history will be rewritten.
- Prompts that simply re-state the system prompts but in a different style. The prompts in `agents/` are **live exports**; paraphrases lose information.

## How to propose

1. Open an issue describing the problem you want to solve.
2. Discuss the design.
3. Open a PR with the smallest possible change.
4. Include:
   - what mode triggers it,
   - what part of the pipeline it touches,
   - what test you ran,
   - what failure modes you considered.

## Style

- Markdown is preferred.
- Diagrams must be SVG, not raster. They must render in GitHub Light, GitHub Dark, on desktop, and acceptably on mobile.
- Examples must show the **mode** used (`QUICK` / `STANDARD` / `DEEP` / `MAX` / `ULTRA`) and at least one citation.

## Code of conduct

Be technical, be specific, be brief. Disagreements to hostile or vague critique will be declined.