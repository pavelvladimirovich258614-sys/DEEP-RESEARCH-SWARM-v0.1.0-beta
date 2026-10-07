# Security Policy

## What this is

DEEP RESEARCH SWARM is a **configuration** of six LobeHub agents + a group system prompt. It is a research aid; it does not run code on your behalf. The repository ships **prompts**, documentation, and SVG diagrams.

## Never commit

If you fork this repository, **never** commit any of:

- API keys (`sk-…`, `sk-ant-…`, `gh[pousr]_…`, `AKIA…`, etc.)
- MCP tokens
- Session cookies
- Bearer tokens (`Bearer …`)
- Passwords in any form
- Private repository content (other people's source code without a license-compatible permission)
- User conversation history
- Personal data (PII): emails, real names of users, private IPs (`10.x`, `172.16–31.x`, `192.168.x`)
- Local filesystem paths (`C:\Users\…`, `/Users/…`)
- LobeHub account identifiers or `agt_…` / `cg_…` / `user_…` / `tpc_…` / `thd_…` IDs that are tied to your personal account
- Telegram bot tokens (`<bot_id>:<30+ chars>`)
- Webhook secrets

The export script we used to assemble this repository scans for all of the above. It is reproduced in `tests/secret-scan.md`.

## If you suspect a leak

Open a private issue or contact the maintainer via the GitHub profile on this repository. **Do not** open a public issue containing the secret.

## What the system itself does to keep secrets out

1. The group prompt forbids agents from emitting API keys, tokens, or personal data into their answers (`PROMPT-INJECTION SHIELD` and `PRIVATE + WEB FUSION`).
2. The Evidence Ledger separates `ORIGIN = PRIVATE | PUBLIC`. Private information is never published as a public source.
3. The Synthesizer is forbidden from inventing citations from memory. It must use the Ledger.
4. The Fact Checker actively hunts for `SEMANTIC CITATION MISMATCH` — for example, a citation about API A used to back a claim about API B.

## Supported versions

This is `v0.1.0-beta`. Security fixes will be backported to `v0.1.x` until `v0.2.0` is released.

## Reporting a vulnerability

Please use GitHub Security Advisories on this repository. Describe:

- what the agent can be made to reveal,
- under what conditions,
- whether you reproduced it.

Do **not** paste the leaked content. A reproducer without the content is enough.