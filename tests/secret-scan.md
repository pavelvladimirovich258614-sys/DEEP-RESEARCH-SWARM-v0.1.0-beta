# Secret scan

This is the **export-time** scan we used to extend DEEP RESEARCH SWARM v0.1.0-beta. It is reproducible: you can run the same checks on your own fork.

The script lives in `tools/scan-secrets.py`. The patterns it checks are below.

## Patterns

| Name | Pattern | Why |
|---|---|---|
| agent_id | `agt_[A-Za-z0-9]+` | a leaked LobeHub agent id ties the file to a personal account |
| group_id | `cg_[A-Za-z0-9]+` | a leaked LobeHub group id ties the file to a personal account |
| user_id | `user_[A-Za-z0-9]+` | a leaked LobeHub user id is a personal identifier |
| topic_id | `tpc_[A-Za-z0-9]+` | conversation topic id |
| thread_id | `thd_[A-Za-z0-9]+` | sub-thread id |
| openai_key | `sk-[A-Za-z0-9]{20,}` | OpenAI API key |
| github_pat | `gh[pousr]_[A-Za-z0-9]{20,}` | GitHub fine-grained token |
| anthropic_key | `sk-ant-[A-Za-z0-9-]{20,}` | Anthropic API key |
| telegram_token | `\d{8,10}:[A-Za-z0-9_-]{30,}` | Telegram bot token |
| windows_path | `[A-Z]:\\Users\\` | Windows home path leaks user name |
| mac_path | `/Users/[A-Za-z]+/` | macOS home path leaks user name |
| email | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | personal email |
| private_ip | `(10|192\.|172\.16–31)\.\d{1,3}\.\d{1,3}\.\d{1,3}` | RFC 1918 IP address |
| http_basic | `https?://[user]:[pass]@` | HTTP basic auth in URL |
| aws_key | `AKIA[0-9A-Z]{16}` | AWS access key |
| named_secret | `(api_key|secret|token|password|bearer|client_secret|refresh_token)[:=][\s\"'][A-Za-z0-9_./+=]{12,}` | any label "secret / token / password" |

## How to run

From the repository root:

```
python tools/scan-secrets.py
```

The script:

1. walks `agents/`, `group/`, `docs/`, `examples/`, `tests/`, `README*.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`;
2. loads each file as text;
3. applies each pattern;
4. reports hits grouped by file and pattern;
5. exits with non-zero status if any hit is found.

## Result for v0.1.0-beta

Run on the date of release:

```
[analyst.txt] (14168 chars): clean
[curator.txt] (22975 chars): clean
[factchecker.txt] (15529 chars): clean
[hunter.txt] (13895 chars): clean
[scout.txt] (12674 chars): clean
[synthesizer.txt] (17287 chars): clean
[group.txt] (39389 chars): clean
Total hits: 0
```

The same scan ran over the entire repository contents (`agents/*.md`, `group/*.md`, `docs/*.md`, `examples/*.md`, `tests/*.md`, the SVG diagrams, the README files in three languages). Result: 0 hits.

## If the scan finds something in your fork

1. Do **not** open a public issue.
2. Rotate the leaked credential.
3. Replace the file with the sanitized version.
4. Re-run the scan. If it is still clean, commit the fix and force-push (and tell anyone who pulled before the leak).