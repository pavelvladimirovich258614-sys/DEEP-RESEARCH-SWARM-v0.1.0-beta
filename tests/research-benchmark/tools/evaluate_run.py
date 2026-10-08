#!/usr/bin/env python3
"""
evaluate_run.py — mechanical metrics for a DEEP RESEARCH SWARM run.

Computes the subset of `rubric.md` metrics that can be derived from the run
artifacts without a human reading the whole transcript:

  3  SOURCE DIVERSITY      -> unique_domains
  5  HALLUCINATION RISK    -> urls_in_final_not_in_agents (candidates, must be verified)
  8  DUPLICATION           -> duplicate_sources, duplication_ratio, agent overlap matrix
  7  AGENT SPECIALIZATION  -> per_agent_source_counts, pairwise overlap
  11 COST / 12 SPEED       -> pass through whatever the platform reported

Metrics that require reading (1 coverage, 4 factuality, 6 contradiction handling,
9 synthesis quality) are NOT computed here. Do not fake them.

Usage:
    python tools/evaluate_run.py RUN_DIR [--out metrics.json]
    python tools/evaluate_run.py --self-test

A RUN_DIR is expected to contain:
    query.txt            the exact question asked
    agent-N.md|agent-N.txt   one file per specialist agent output
    group-result.md      the final Synthesizer answer
    timings.json         optional: {"agents": {"scout": 12.3, ...}, "total": 71.2}

Design rules:
- Never invents numbers. Unavailable fields stay null.
- Exit code 0 on success, 1 on a usage/input error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

AGENT_FILE_RE = re.compile(r"^agent[-_](?P<name>[A-Za-z0-9_\-]+)\.(md|txt)$")
URL_RE = re.compile(r"https?://[^\s\)\]\}\"'<>`]+")
TRAILING_PUNCT_RE = re.compile(r"[.,;:!?]+$")

# Hosts that indicate a primary/authoritative source class.
PRIMARY_HOST_HINTS = (
    "arxiv.org", "doi.org", "github.com", "gitlab.com", "bitbucket.org",
    "docs.", "documentation", "readthedocs.io", "developer.", "api-docs",
    ".gov", ".edu", "europa.eu", "w3.org", "ietf.org", "rfc-editor.org",
    "sqlite.org", "postgresql.org", "python.org", "kernel.org", "rust-lang.org",
    "mozilla.org", "chromium.org", "microsoft.com", "openai.com", "anthropic.com",
)
SECONDARY_HOST_HINTS = (
    "medium.com", "substack.com", "blog.", "news.", "dev.to", "hashnode.dev",
    "infoq.com", "thenewstack.io", "restofworld.org", "wired.com", "techcrunch.com",
    "theverge.com", "arstechnica.com", "zdnet.com",
)
COMMUNITY_HOST_HINTS = (
    "reddit.com", "news.ycombinator.com", "stackoverflow.com", "stackexchange.com",
    "quora.com", "twitter.com", "x.com", "discord", "slack.com", "lobste.rs",
)


def _strip_punct(url: str) -> str:
    return TRAILING_PUNCT_RE.sub("", url)


def _normalise(url: str) -> str:
    """Normalise for identity comparison: lower-case host, no fragment, no
    common tracking params, no trailing slash."""
    url = _strip_punct(url)
    try:
        p = urlparse(url)
    except ValueError:
        return url.lower()
    if not p.netloc:
        return url.lower()
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = (p.path or "").rstrip("/")
    query = ""
    if p.query:
        kept = [
            kv for kv in p.query.split("&")
            if kv and not kv.lower().startswith(("utm_", "ref=", "source="))
        ]
        query = "&".join(sorted(kept))
    base = f"{host}{path}"
    return f"{base}?{query}" if query else base


def _netloc(url: str) -> str:
    """urlparse().netloc that also works on scheme-less normalised URLs
    (e.g. "github.com/proj"), which is what _normalise() returns."""
    u = _strip_punct(url)
    try:
        if "//" not in u.split("?")[0][:10]:
            u = "//" + u
        return urlparse(u).netloc.lower()
    except ValueError:
        return ""


def _domain(url: str) -> str:
    host = _netloc(url)
    return host[4:] if host.startswith("www.") else host


def _classify(host: str) -> str:
    if not host:
        return "UNKNOWN"
    if any(h in host for h in COMMUNITY_HOST_HINTS):
        return "COMMUNITY"
    if any(h in host for h in PRIMARY_HOST_HINTS):
        return "PRIMARY"
    if any(h in host for h in SECONDARY_HOST_HINTS):
        return "SECONDARY"
    return "SECONDARY"


def extract_urls(text: str) -> list[str]:
    return [_strip_punct(u) for u in URL_RE.findall(text or "")]


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def discover_agent_files(run_dir: str) -> dict[str, str]:
    agents: dict[str, str] = {}
    for entry in sorted(os.listdir(run_dir)):
        m = AGENT_FILE_RE.match(entry)
        if m:
            agents[m.group("name")] = os.path.join(run_dir, entry)
    return agents


def evaluate(run_dir: str) -> dict:
    if not os.path.isdir(run_dir):
        raise FileNotFoundError(f"run dir not found: {run_dir}")

    agent_files = discover_agent_files(run_dir)
    if not agent_files:
        raise ValueError(
            "no agent-N.md / agent-N.txt files found; cannot compute metrics"
        )

    agent_urls: dict[str, set[str]] = {}
    all_urls: set[str] = set()

    for name, path in agent_files.items():
        urls = {_normalise(u) for u in extract_urls(_read(path))}
        agent_urls[name] = urls
        all_urls |= urls

    final_path = None
    for cand in ("group-result.md", "group-result.txt"):
        if os.path.exists(os.path.join(run_dir, cand)):
            final_path = os.path.join(run_dir, cand)
            break
    final_urls = {_normalise(u) for u in extract_urls(_read(final_path))} if final_path else set()

    # Source classes and domain diversity across the whole run.
    counts = Counter(_classify(_domain(u)) for u in all_urls)
    domains = {_domain(u) for u in all_urls}
    domains.discard("")

    # Duplication: a URL found by more than one agent.
    seen_by: dict[str, list[str]] = defaultdict(list)
    for name, urls in agent_urls.items():
        for u in urls:
            seen_by[u].append(name)
    duplicate_sources = sum(1 for u, agents in seen_by.items() if len(agents) > 1)

    # Hallucination candidates: URLs in the final answer that no agent produced.
    candidates = sorted(final_urls - all_urls)

    # Pairwise agent overlap (Jaccard) — low overlap is healthy.
    overlap: dict[str, float] = {}
    names = sorted(agent_urls)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sa, sb = agent_urls[a], agent_urls[b]
            if not sa and not sb:
                continue
            union = sa | sb
            overlap[f"{a}|{b}"] = round(len(sa & sb) / len(union), 4) if union else 0.0

    total_agent_urls = sum(len(v) for v in agent_urls.values())
    duplication_ratio = (
        round(duplicate_sources / total_agent_urls, 4) if total_agent_urls else None
    )

    timings = {}
    tpath = os.path.join(run_dir, "timings.json")
    if os.path.exists(tpath):
        try:
            raw = json.loads(_read(tpath))
            timings = {
                "runtime_seconds": raw.get("total"),
                "per_agent_seconds": raw.get("agents", {}),
                "source": "run artifact timings.json",
            }
        except (ValueError, OSError) as exc:
            timings = {"error": f"timings.json unreadable: {exc}"}

    return {
        "schema": "swarm-eval/1.0",
        "run_dir": os.path.abspath(run_dir),
        "agents_detected": len(agent_files),
        "sources_found": len(all_urls),
        "unique_domains": len(domains),
        "domains": sorted(domains),
        "source_classes": {
            "primary": counts.get("PRIMARY", 0),
            "secondary": counts.get("SECONDARY", 0),
            "community": counts.get("COMMUNITY", 0),
            "unclassified": counts.get("UNKNOWN", 0),
            "note": (
                "Heuristic, host-based only. A domain is not evidence quality; "
                "verify each load-bearing citation by hand before scoring "
                "metric 2 (SOURCE QUALITY)."
            ),
        },
        "per_agent_source_counts": {
            name: len(urls) for name, urls in sorted(agent_urls.items())
        },
        "duplicate_sources": duplicate_sources,
        "duplication_ratio": duplication_ratio,
        "agent_overlap_jaccard": overlap,
        "final_answer_urls": len(final_urls),
        "urls_in_final_not_in_agents": {
            "count": len(candidates),
            "urls": candidates,
            "note": (
                "HALLUCINATION CANDIDATES, not proven hallucinations. A citation "
                "written during synthesis that no agent produced is the classic "
                "signature, but verify each one before recording a metric 5 failure."
            ),
        },
        "cost": {
            "input_tokens": None,
            "output_tokens": None,
            "note": "Left null on purpose. Do not estimate tokens from text length.",
        },
        "speed": timings or {
            "runtime_seconds": None,
            "per_agent_seconds": {},
            "note": "No timings.json in the run dir.",
        },
        "errors": [],
        "not_computed_here": [
            "1 COVERAGE", "4 FACTUALITY", "6 CONTRADICTION HANDLING",
            "9 FINAL SYNTHESIS", "10 CITATION QUALITY",
            "13 FAILURE RECOVERY",
        ],
    }


def _self_test() -> int:
    """Minimal sanity test with synthetic artifacts. No network, no LLM calls."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "query.txt").write_text("What is X?", encoding="utf-8")
        (root / "agent-scout.md").write_text(
            "Found https://example.com/a and https://github.com/proj", encoding="utf-8"
        )
        (root / "agent-hunter.md").write_text(
            "Verified https://github.com/proj, https://arxiv.org/abs/1234 "
            "and community report https://reddit.com/r/example",
            encoding="utf-8",
        )
        (root / "group-result.md").write_text(
            "Per https://example.com/a and https://fabricated.invalid/xyz",
            encoding="utf-8"
        )
        m = evaluate(d)

    checks = [
        ("agents_detected", m["agents_detected"], 2),
        ("unique_domains", m["unique_domains"], 4),
        ("duplicate_sources", m["duplicate_sources"], 1),
        ("hallucination_candidates", m["urls_in_final_not_in_agents"]["count"], 1),
        ("primary_counted", m["source_classes"]["primary"] >= 2, True),
        ("community_counted", m["source_classes"]["community"] >= 1, True),
    ]
    ok = True
    for label, got, want in checks:
        good = got == want
        ok &= good
        print(f"{'PASS' if good else 'FAIL'}  {label}: got={got!r} want={want!r}")
    print("\nself-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", nargs="?", help="directory holding one run's artifacts")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    ap.add_argument("--self-test", action="store_true", help="run synthetic sanity test")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()
    if not args.run_dir:
        ap.print_help()
        return 1

    try:
        metrics = evaluate(args.run_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    payload = json.dumps(metrics, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
        print(f"wrote {args.out}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())