"""Reproducible export-time secret scanner for DEEP RESEARCH SWARM v0.1.0-beta.

Walks agents/, group/, docs/, examples/, tests/, the root files, and the SVG
diagrams. Applies a set of patterns. Prints hits grouped by file and pattern.
Exits non-zero if any hit is found.

Run from the repository root:
    python tools/scan-secrets.py
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGET_DIRS = ["agents", "group", "docs", "examples", "tests", "assets"]
TARGET_FILES = ["README.md", "README.ru.md", "README.zh-CN.md",
                "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md"]

PATTERNS = {
    # IDs that are obvious placeholders (literal "xxx") are excluded.
    "agent_id_live":  re.compile(r"agt_(?!xxx\b)[A-Za-z0-9]{4,}"),
    "group_id_live":  re.compile(r"cg_(?!xxx\b)[A-Za-z0-9]{4,}"),
    "user_id_live":   re.compile(r"user_(?!xxx\b|id\b)[A-Za-z0-9]{4,}"),
    "topic_id":       re.compile(r"tpc_[A-Za-z0-9]{4,}"),
    "thread_id":      re.compile(r"thd_[A-Za-z0-9]{4,}"),
    "openai_key":     re.compile(r"sk-(?!ant-)[A-Za-z0-9]{20,}"),
    "github_pat":     re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "anthropic_key":  re.compile(r"sk-ant-[A-Za-z0-9-]{20,}"),
    "telegram_token": re.compile(r"\d{8,10}:[A-Za-z0-9_-]{30,}"),
    "windows_path":   re.compile(r"[A-Z]:\\Users\\[A-Za-z0-9 _\\-]+", re.I),
    "mac_path":       re.compile(r"/Users/[A-Za-z]+/[A-Za-z0-9_/]+"),
    "email":          re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "private_ip":     re.compile(r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "http_basic":     re.compile(r"https?://[A-Za-z0-9_.-]+:[A-Za-z0-9_!@#$%^&*()-]+@[A-Za-z0-9._-]+"),
    "aws_key":        re.compile(r"AKIA[0-9A-Z]{16}"),
    "named_secret":   re.compile(r"(?i)(api[_-]?key|apikey|secret|token|password|passwd|bearer|client_secret|access_token|refresh_token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+=]{12,}"),
}

total_hits = 0

paths = []
for d in TARGET_DIRS:
    p = os.path.join(ROOT, d)
    if os.path.isdir(p):
        for root, _, files in os.walk(p):
            for fn in files:
                paths.append(os.path.join(root, fn))
for f in TARGET_FILES:
    p = os.path.join(ROOT, f)
    if os.path.isfile(p):
        paths.append(p)

paths = sorted(paths)
for p in paths:
    try:
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        continue
    hits = {}
    for name, pat in PATTERNS.items():
        m = pat.findall(text)
        if m:
            sample = sorted({x if isinstance(x, str) else x[0] for x in m})[:5]
            hits[name] = sample
    rel = os.path.relpath(p, ROOT)
    if hits:
        total_hits += sum(len(v) for v in hits.values())
        print(f"\n[{rel}]")
        for k, vals in hits.items():
            print(f"  ⚠ {k}: {vals}")
    else:
        print(f"[{rel}] clean")

print(f"\nTotal hits: {total_hits}")
sys.exit(0 if total_hits == 0 else 1)