# M45-ST/31 — Auditable GitHub-native computation

This stage adds two **separate** verification paths:

1. `verify_journal.py` replays the ST30 fixed-table unary Turing machine from a pinned genesis state through every JSONL transition record and checks the saved tape against the replayed result.
2. `verify_sk.cjs` independently recomputes ST29 browser SK traces and checks their contents, step count, result, and status.

GitHub Actions `m45-st31-audit.yml` runs both audit suites and their tests without write permissions.

## Local verification

```sh
python3 m45-st31/verify_journal.py
python3 -m unittest discover -s m45-st31 -p 'test_*.py'
node m45-st31/test_sk.cjs
node m45-st31/verify_sk.cjs path/to/m45-st29-certificate.json
```

## Limitations

- The ST30 fixed-transition-table machine and ST29 SK browser evaluator remain **distinct**. This is not a proof that the SK evaluator is implemented by the fixed-table TM.
- Journal replay starts from a known genesis state. SHA-256 detects changes relative to that genesis and table but is not a digital signature or proof against an attacker with control of the repository and verifier.
- ST30's state-writing workflow does not yet invoke this audit **before** advancing the tape. The ST31 audit workflow checks the history separately. Do not treat an unverified state write as validated.
- SK browser certificates are downloaded locally; no automated persistent SK Git commits or GitHub Pages publication is claimed.
- GitHub-hosted resources are finite. This system is not a mathematical infinite-tape computer, a halting oracle, or a physically real Doraemon.
- This branch depends on ST30, ST29 and ST28; merge those in order and run GitHub Actions before making claims of deployed functionality.
