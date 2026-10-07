# Tools and skills

> Each agent lists what it actually uses. None of the agents invent tools — they use what's configured in LobeHub.

## Built-in LobeHub plugins used by this group

| Plugin id | Used by | Why |
|---|---|---|
| `lobe-web-browsing` | Curator, Scout, Hunter, Analyst, Fact Checker | primary search + crawl |
| `lobe-browser` | Curator, Scout, Hunter, Fact Checker | visual browsing when login/JS is required |
| `lobe-agent-browser` | Scout, Hunter, Analyst, Fact Checker | browser-side automation in browser sidebar |
| `lobe-agent-documents` | Curator, Analyst, Fact Checker, Synthesizer | persistent Evidence Ledger, Claim Graph, Source Graph |
| `lobe-agent-management` | Curator, Synthesizer | cross-agent coordination, group editing |
| `lobe-artifacts` | Curator, Analyst, Fact Checker, Synthesizer | diagrams, tables, formatted final outputs |
| `lobe-cloud-sandbox` | Hunter, Analyst | run small scripts / CLI checks when needed |
| `lobe-computer-use` | Synthesizer (optional) | longer/more complex report writing |
| `lobe-message` (optional) | any agent that needs IM history | read/write messages across supported channels |
| `lobe-task` (optional) | Curator | break the run into trackable tasks |

## Optional marketplace integrations (recommended per use case)

| Plugin | When |
|---|---|
| `github` | for GitHub-Discovery workstreams (scoring repos, scanning issues, verifying commit dates) |
| `twitter` (X) | for community-signal queries ("do users complain about X?") |
| `pollinations-pollinations-web-research` | additional discovery channel |
| `firecrawl-*, tavily-*, camoufox-research-*` | when you need deeper page content than `lobe-web-browsing` provides |
| `notion` / `linear` / `google-docs` | when you want the final report archived in your workspace |
| Composio integrations (Gmail, Slack, etc.) | only if a specific task requires them |

## How tool capability is bound

- LobeHub binds tools **per agent**, not per group. The Curator cannot borrow a tool that is only on the Hunter's profile, and vice versa.
- A specialist that wants to call a tool it does not have should report this to the Curator and let the Curator route the call to an agent that does have it.

## What an agent MUST NOT do with a tool

- **No recursive delegation.** A specialist may not use `lobe-agent-management` to spawn a sub-agent.
- **No tool-call batching in parallel phase.** Inside `Scout ∥ Hunter`, each agent issues at most **one** tool/skill call per turn. This is what prevents "orphaned skill call" warnings.
- **No tool-call replay.** A failed primary call must be **closed** with its terminal result (even if it's an error) before the fallback runs in a separate turn.
- **No "fake" tools.** Agents must not invoke skills or tools that do not exist (orphaned calls by name). The system protocol is honest about NATIVE / EMULATED / NOT SUPPORTED.

## Skills (research-domain specific)

Skills are recommended, not required. The system works without any skills if the standard plugin set is enabled.

- `web-research` (Pollinations-style) — fallback discovery channel
- `firecrawl-search`, `tavily-search` — additional search backends
- `camoufox-research-deep-research` — when many pages need to be opened in parallel
- `market-research` (Montelo / Cohere) — for finance / market sizing
- `agent-reach` — for social-media platforms
- `pdf` / `anthropic-pdf` — for PDFs the standard browser cannot read
- `skill-creator` — to codify repeatable skills

> The skill catalogue evolves. Pick the minimum needed for the question; do not blanket-enable everything.

## Model recommendations (model-agnostic system)

The repository is **model-agnostic**. The live configuration used at the time of v0.1.0-beta is described below as an example only.

| Role | Property | Example (live) |
|---|---|---|
| Curator / Hunter / Analyst / Fact Checker | strong planning, tool-calling, large context | `MiniMax-M3` or equivalent |
| Scout | fast, low-latency, good tool-calling | `Qwen3.8-flash` or equivalent |
| Synthesizer | long-context + writing | `Qwen3.8-flash` or equivalent (long-context variant preferred) |

The exact models in the live group were:

| Agent | Model |
|---|---|
| Curator | `mistral-large-4` |
| Wide Web Scout | `qwen3.8-flash` |
| Primary Source Hunter | `MiniMax-M3` |
| Evidence Analyst | `MiniMax-M3` |
| Fact Checker / Red Team | `MiniMax-M3` |
| Research Synthesizer | `qwen3.8-flash` |

These are sample choices. You can swap any of them; the architecture does not depend on them.