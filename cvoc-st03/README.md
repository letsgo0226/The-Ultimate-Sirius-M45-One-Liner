# CVOC-ST03 Native Verification Audit

Read-only integration tests call the **actual** native ST30, ST38, ST43, ST44 and ST47 Python modules from the same checked-out Git commit. Tests use in-memory sample data and do not modify repository state or call any external service.

This branch is stacked on `feature/m45-st47-single-writer-state` and its PR must target that branch. Do not merge independently into `main` before the ST dependency chain is reviewed.

Run locally: `python3 -m unittest discover -s cvoc-st03 -p 'test_*.py' -v`.

Scope: six tests covering bounded ST30 transition, ST38 replay/tamper, ST43 native memory verification, ST44 pocket binding, ST47 state envelope and explicit schema incompatibility. This does **not** prove arbitrary cross-machine state conversion, external provenance, cryptographic authentication, continuous runtime, or deployment. CI result must be checked before claiming success. No schedule, write token, secret, or state branch is enabled.
