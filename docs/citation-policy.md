# Citation policy

Every factual claim in the final report must have a citation that has passed a five-step verification.

## The five-step verification

```
URL exists ?
   |
   v
page was actually opened ?
   |
   v
page contains the claimed fact ?
   |
   v
page version / date is relevant ?
   |
   v
page is not a paraphrase / repost / SEO spam ?
```

Any `no` → `CITATION FAIL`.

## Where citations live

- For each claim in the final answer, the Synthesizer attaches the canonical URL and a passage locator (section / heading / line / commit hash).
- For a single page that supports several claims, the citation is repeated at each claim so that the citation is **right next to** the claim, not aggregated at the end of the report.
- For sources behind paywalls or login walls, the Agent falls back to archive.org and marks the citation `ARCHIVE` in the research audit.

## What counts as a valid citation

| Source class | Valid for |
|---|---|
| Official docs / site | product capability, contract, supported platforms |
| Official repository | version, license, releases, repo health, API examples |
| Official paper / arXiv preprint | methodology, benchmarks (with `SELF-REPORTED` flag) |
| Maintainer issue comment / maintainer ack | technical claims about the project's behaviour |
| Filings / press releases | corporate facts, dates, financials |
| Trusted media (in `KNOWN_PRIMARY_DOMAINS`) | company news, market context |
| Community (Reddit / HN / forum) | community sentiment only; never a technical fact |

## What does NOT count as a valid citation

- AI-generated scraped articles that just rephrase Wikipedia.
- Anonymous SEO blogs with no source attribution.
- Documentation mirrors that lag behind the upstream by more than one minor version, unless explicitly noted.
- GitHub stars used as a quality argument.
- Synthetic benchmarks whose dataset, model, methodology or evaluation metric is not disclosed.

## Repository health fields

For each software repository cited, the final report may include:

- `STARS` — adoption signal only
- `LAST_PUSH` — `pushed_at` from GitHub API (the **latest** push to any branch)
- `LAST_COMMIT` — only from `commits` API on the default branch; otherwise `NOT VERIFIED`
- `REPO_UPDATED_AT` — `updated_at` (any change, including settings)
- `LATEST_RELEASE` — `releases/latest` or `tags?per_page=1`
- `OPEN_ISSUES` — `open_issues_count`
- `CONTRIBUTORS` — only from `contributors` API or page; otherwise `NOT VERIFIED`
- `LICENSE` — `license` field
- `ARCHIVED` — `archived` flag
- `RELEASE_CADENCE` — derived from the release history

> `LAST_COMMIT` ≠ `pushed_at`. The Ledger must keep them separate. A "no push in 12 months" finding is reported as `LAST_PUSH` ≥ 12 months ago, **not** as "no commits".

## Citation Coverage Score

Before the final report is shipped, the Fact Checker computes:

```
IMPORTANT_CLAIMS          = N
CLAIMS_WITH_VALID_CITATION = M
CITATION_COVERAGE_SCORE   = M / N
```

For `DEEP` and above, the target is `CITATION_COVERAGE_SCORE = 1.0` for factual claims. Otherwise the run returns `FAIL` with the gaps listed.

## Citation Entitlement

One citation supports **only** the closest claim. A source about "this product has a Windows installer" does not also prove "this product has Deep Research". The Fact Checker is required to detect `SEMANTIC CITATION MISMATCH` and FAIL the run if found.

## UNKNOWN / NOT VERIFIED are valid

If something cannot be verified, the report says so. The user can read `NOT VERIFIED` as "we looked, we couldn't confirm, here's the closest we got, here is why". This is preferable to inventing a citation that doesn't satisfy the five-step verification.