# Run evaluation — <task id> <task title>

Copy to `benchmark-results/run-NNN/evaluation.md` and fill in after the run.

Run id:
Task id:
Mode used (expected):
Date of run:

## Verdict table

| # | Metric | Score | PASS/FAIL/UNKNOWN | Evidence |
|---|---|---|---|---|
| 1 | COVERAGE | | | |
| 2 | SOURCE QUALITY | | | |
| 3 | SOURCE DIVERSITY | | | |
| 4 | FACTUALITY | | | |
| 5 | HALLUCINATION RISK | | | |
| 6 | CONTRADICTION HANDLING | | | |
| 7 | AGENT SPECIALIZATION | | | |
| 8 | DUPLICATION | | | |
| 9 | FINAL SYNTHESIS | | | |
| 10 | CITATION QUALITY | | | |
| 11 | COST | | | |
| 12 | SPEED | | | |
| 13 | FAILURE RECOVERY | | | |

## Mechanical counters

Paste the output of:

```
python tests/research-benchmark/tools/evaluate_run.py benchmark-results/run-NNN
```

- sources_found:
- unique_domains:
- duplicate_sources:
- urls_in_final_not_in_agents:
- runtime_seconds:

## Highest-severity defect

One line. If there is no defect, write `none` — do not leave it blank, because a
blank reads as "not checked".

## Injected failures and recovery

| Failure injected | Expected | Observed | Verdict |
|---|---|---|---|
| | | | |

## Blocking-metric check

The four blocking metrics are 2, 4, 5 and 10.

- Blocking failures:
- Eligible for comparison with other runs (task id + mode + complete metrics.json): yes / no

## Notes

Anything the mechanical counters cannot see: which agent did what, where the swarm
drifted, which required_signals from `benchmark.json` were missed.