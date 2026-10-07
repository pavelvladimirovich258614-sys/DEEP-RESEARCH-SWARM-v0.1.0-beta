# Evidence Ledger

The Evidence Ledger is the **single source of truth** for everything the Synthesizer writes. If a claim is not in the ledger, it must not appear in the final report.

## Record schema

| Field | Type | Description |
|---|---|---|
| `CLAIM_ID` | string | stable id like `LLD-A1`, `LLD-A2-B7` (hierarchical) |
| `CLAIM` | string | the claim itself, written as a single factual sentence |
| `TYPE` | enum | one of `FACT` · `SOURCE CLAIM` · `INTERPRETATION` · `INFERENCE` · `COMMUNITY EXPERIENCE` · `UNKNOWN` · `ABSENCE OF EVIDENCE` |
| `EVIDENCE` | text | the relevant passage, quoted verbatim (extract not paraphrase) |
| `SOURCE` | string | domain or repository / paper title |
| `URL` | URL | canonical URL with version/branch hint where relevant |
| `PASSAGE` | locator | section / heading / commit / line number where the evidence lives |
| `VERSION` | string | product / version / commit hash (when relevant) |
| `PUBLICATION_DATE` | ISO date | when the source was published |
| `RETRIEVED_DATE` | ISO date | when the passage was opened |
| `CLASS` | enum | `PRIMARY` · `SECONDARY` · `COMMUNITY` |
| `SOURCE_QUALITY` | enum | `HIGH` · `MEDIUM` · `LOW` |
| `CONFIDENCE` | enum | `HIGH` · `MEDIUM` · `LOW` |
| `STATUS` | enum | `VERIFIED` · `LIKELY` · `CONTESTED` · `NOT VERIFIED` · `UNKNOWN` |
| `VERDICT` | enum | `SUPPORTED` · `PARTIAL` · `UNSUPPORTED` |
| `CONTRADICTING_EVIDENCE` | text | passages that disagree with the claim, if any |
| `NOTES` | text | any caveats, including `SELF-REPORTED`, `INFERENCE`, `STALE`, `BENCHMARK NOT COMPARABLE` |

## Example row

```
CLAIM_ID:    LLD-A1
CLAIM:       docling is an MIT-licensed document-to-Markdown pipeline maintained by Docling-Project
TYPE:        source CLAIM
EVIDENCE:    "Apache-2.0 license header in the repository; project page describes
             the converter as open-source under MIT"
SOURCE:      github.com/DS4SD/docling
URL:         https://github.com/DS4SD/docling
PASSAGE:     README + LICENSE
VERSION:     latest release at retrieval
PUBLICATION_DATE: 2025-09-15
RETRIEVED_DATE:   2026-10-07
CLASS:       PRIMARY
SOURCE_QUALITY: HIGH
CONFIDENCE:  HIGH
STATUS:      VERIFIED
VERDICT:     SUPPORTED
CONTRADICTING_EVIDENCE: —
NOTES:       LICENSE confirmed by direct repository access.
```

## Confidence ladder

| Confidence | Rule |
|---|---|
| `HIGH` | primary source + independent confirmation + fresh data |
| `MEDIUM` | good secondary source, or community + supporting evidence |
| `LOW` | one community report, a snippet, an unverified benchmark, or an indirect inference |

A critical claim with `LOW` confidence **cannot** be the basis of a recommendation.

## Types, defined

- **FACT** — directly observable, evidence is the observation itself (e.g., GitHub API returning `pushed_at = 2025-08-22`).
- **SOURCE CLAIM** — a documented statement in a primary source (README, docs, paper, release notes). The source has the authority; we are reporting it.
- **INTERPRETATION** — a label derived from facts (e.g., "the project looks abandoned" derived from no push in 12 months). Must be labelled, not passed off as a fact.
- **INFERENCE** — a logical conclusion from multiple facts (e.g., "X supports feature Y because the docs describe the integration"). Must be supported.
- **COMMUNITY EXPERIENCE** — what users say (issues, Reddit, forum posts). Not a technical fact unless independently confirmed.
- **UNKNOWN** — no usable evidence at all.
- **ABSENCE OF EVIDENCE** — the source was inspected and the claim was not documented. **Never** collapse this into `NO`. Absence of evidence is not evidence of absence.

## Negative claim rule

Negative claims (`NO`, `NOT SUPPORTED`, `ONLY`, `NEVER`, `ALWAYS`, `REQUIRED`, `IMPOSSIBLE`, `CLOUD-ONLY`, `ABANDONED`, `BEST`, `WORST`) require strong evidence. The default for "the README does not mention Ollama" is `Ollama: NOT DOCUMENTED`, **not** `Ollama: NO`.

## Windows / local / own-models semantics

For software research the Ledger must separate the deployment planes:

- `APP_HOSTING` — local Node.js / Python / native binary / Docker
- `LLM_INFERENCE` — local Ollama / LM Studio / cloud API
- `SEARCH_BACKEND` — local SearXNG / cloud Firecrawl / etc.
- `DATA_STORAGE` — local SQLite / managed cloud DB

A common mistake is collapsing these into a single "cloud only" / "local" answer. Keep them separate.

## Community ≠ fact

A community report (Reddit, GitHub issue, forum thread) is **not** a technical fact. To promote it to fact, the Analyst must have at least one of:

- GitHub issue with a reproducer,
- maintainer acknowledgement,
- changelog / fix entry,
- multiple independent confirmations.

Otherwise the wording in the final answer stays "**some users report …**".

## Claim Graph (above the ledger)

The Analyst also maintains a Claim Graph:

```
CLAIM_ID | SUPPORTS | CONTRADICTS | DEPENDS_ON | DERIVED_FROM | CONFIDENCE
```

Rule: if claim `X` is `FAIL`, every claim that `DEPENDS_ON X` is re-examined.

## Entity Graph

For complex comparisons (multiple products, multiple versions), the Analyst maintains an Entity Graph:

```
ENTITY: PRODUCT | COMPANY | VERSION | MODEL | PERSON | ORGANIZATION | REPOSITORY | PAPER | FEATURE
RELATIONS: MAINTAINED_BY | DEPENDS_ON | COMPETES_WITH | REPLACED_BY | FORK_OF | RENAMED_TO | USES
```

This prevents confusing similarly-named projects (e.g., "Perplexica" vs "Perplexity", "Open Deep Research" by LangChain vs an unrelated repo).