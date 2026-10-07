# Example 3 — GitHub-first research

> Mode: 🔎 DEEP

## User query

> Find the best open-source alternative to Perplexity for self-hosting. I want code on GitHub, license compatible with closed-source work, last push within 12 months, MCP or HTTP API, and a Docker image.

## Why "GitHub-first"?

The user constraints are **provenance-first** constraints:

- code on GitHub → primary source is the repo
- license compatibility → primary source is the LICENSE file
- last push within 12 months → `pushed_at` (NOT `LAST_COMMIT`)
- MCP or HTTP API → primary source is the README
- Docker image → primary source is the Dockerfile / docker-compose / registry

The Scout has limited value; the **Hunter** does most of the work.

## Hunter's checklist per candidate

```
repo           = X/Y
license        = spdx
last_push      = pushed_at
last_commit    = commits API default branch (optional)
latest_release = releases/[latest]/tag_name
open_issues    = open_issues_count
docker_image   = present? README says so?
mcp_or_http    = ?
archived       = False
contributors   = from contributors API (NOT inferred)
```

The Hunter returns a short list (3–6 candidates) that pass the basic gates. Anything failing the freshness gate is demoted with `STALE — no push in N months`.

## What the Analyst checks

- For each candidate: read the README, extract passages for **each** claim (Docker, MCP, license, languages).
- Build the Claim Graph: `Docker SUPPORTED | MCP SUPPORTED | LICENSE OK | FRESHNESS OK | RU+EN OK | PASS 5 host OS variants`.
- Build the Entity Graph: distinguish projects with similar names (e.g., "Perplexica" ≠ "Perplexity"; "Open Deep Research" by LangChain vs unrelated repos with the same name).

## What the Fact Checker verifies

For each cell in the comparison table, the five-step verification:

1. URL exists?
2. Page was opened?
3. Page contains the claim?
4. Page version/date is the relevant one?
5. Page is not a paraphrase?

If any `no`, the row is `CITATION FAIL` → gate the table.

## What the final answer contains

A comparison table with rows that pass the gate; a primary recommendation; a Pareto-optimal shortlist (`BEST LOCAL | BEST EASY SETUP | BEST RU+EN | BEST FREE`); a research audit with the freshness gate verdicts.

## Important semantics

- `pushed_at` → `LAST_PUSH`.
- `LAST_COMMIT` is **only** from `commits` API on the default branch.
- "Last commit 12 months ago" is wrong if `pushed_at` was last week.
- "Stars = quality" is wrong. Stars = adoption signal.
- "License MIT" is right only if the LICENSE file says MIT.