# M45-ST/82 — Relational Quantum Scientific Verification and Evidence Ledger

ST81 introduced cross-stage execution and determinism checks. ST82 turns those checks into a **conservative, source-bound evidence ledger** that distinguishes *code present*, *execution evidence verified*, and *scientific truth established*. These are different epistemic categories.

## Ledger protocol

The ledger contains one scoped claim per audited stage: ST64, ST68, ST69 and ST73–ST80. Each record includes a precise source path, its current SHA-256 hash, the claim's intended scope, explicit limitations, a matching ST81 output hash (if available), and machine-readable checks:

1. Source exists in the current checkout.
2. An ST81 audit entry exists and records a successful run.
3. The source hash in the audit matches the current file.
4. A syntactically valid SHA-256 output hash is present.
5. Repeated execution was recorded as deterministic, with matching output hashes.
6. The stage's unittest result passed (default requirement).

The record becomes `AUDIT_VERIFIED` **only if every required check passes**. Otherwise it remains `UNVERIFIED`; missing audit evidence never counts as success. This is a verification of *reported execution/repeatability evidence*, **not** independent mathematical proof or scientific validation.

## Reproducible commands

```sh
python3 -m unittest discover -s m45-st82 -p 'test_*.py'
python3 m45-st81/reproducibility_audit.py --run-tests --output m45-st81-audit.json
python3 m45-st82/evidence_ledger.py --audit m45-st81-audit.json --output m45-st82-ledger.json
python3 m45-st82/evidence_ledger.py --audit m45-st81-audit.json --require-verified
```

The GitHub Actions workflow attempts ST81 auditing even if some stages fail, generates the ledger from available evidence, uploads both JSON reports, and then **fails the job unless all required audit records are verified**. No secrets or write permissions are required.

## Evidence hierarchy and limits

- **UNVERIFIED:** no matching passing audit evidence; this does not necessarily mean a theory is false.
- **AUDIT_VERIFIED:** a successful deterministic execution and unit-test result is recorded for the checked-out source under the specified runtime and arguments.
- **Scientific validity:** not established by either status; requires independent assumptions, proof review, statistical validation, and where applicable physical experimentation.

The ST81 audit report is trusted as a local artifact; this ledger does **not** authenticate signatures, attest GitHub runners, or protect against a forged audit JSON. Source hashes guard against accidental source-version mismatch, not adversarial tampering. Claims about quantum hardware, new physical laws, general reference frames, autonomous open-ended discovery and metaphysical theorems remain explicitly **not established**. The ledger is an epistemic accounting tool, not an oracle.

CI and external review pending.
