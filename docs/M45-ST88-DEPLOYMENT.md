# M45-ST/88 — Gödel Autonomous Thought Engine

## What this does
An internally clocked deterministic state-transition demonstrator. It does not require incoming chat messages for each transition, uses reversible base-257 byte+1 Gödel encoding, and does not use SHA or hashlib.

## Run
```sh
python3 -m unittest -v test_m45_st88.py
python3 m45_st88.py
```
Stop with Ctrl+C. The default runtime has no preset duration limit, but execution depends on the host, power, and operating system.

## CI
The GitHub Actions workflow runs a **bounded** 3-step smoke test. It intentionally does not start an endless GitHub Actions job. No production secrets or privileged tokens are required.

## Proposed always-on hosting (not deployed)
Use a low-privilege process supervisor with restart-on-failure, bounded log retention, storage quotas, explicit monthly budget alerts, and a manual stop/kill switch. Persist state only after an integrity/recovery design review. Do not claim 24/7 availability until an actual hosted service is provisioned and observed.

## Governance
ST/88 is a draft PR based on ST/87. Independent human review and the upstream PR chain remain required. No automatic merging or production deployment. This computational model does not establish consciousness, subjective experience, or infinite operation.
