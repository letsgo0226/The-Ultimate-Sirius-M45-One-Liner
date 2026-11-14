# M45-ST/85 — Scientific Integrity and Constitutional Constraints

ST85 adds a **fail-closed integrity verifier** for the ST81→ST82→ST83→ST84 evidence chain. It checks whether each JSON document uses the expected protocol, whether the governance artifact is cryptographically bound by SHA-256 to the plan, whether every review decision references a source task, whether evidence statuses agree with recorded checks and audit results, and whether approval/execution flags remain disabled.

## Constitutional rules

1. No automatic approval, merge, source modification, deployment, or arbitrary command execution.
2. No declaration of scientific truth from software execution alone.
3. Evidence claims marked verified must be consistent with audit and test records.
4. A governance decision must refer to an unchanged ST83 proposal and remain pending human review.
5. Unexpected document formats, broken bindings, contradictory statuses or permission escalation produce a nonzero exit code.

## Usage

```sh
python3 -m unittest discover -s m45-st85 -p 'test_*.py'
python3 m45-st81/reproducibility_audit.py --run-tests --output m45-st81-audit.json
python3 m45-st82/evidence_ledger.py --audit m45-st81-audit.json --output m45-st82-ledger.json
python3 m45-st83/epistemic_correction.py --ledger m45-st82-ledger.json --output m45-st83-plan.json
python3 m45-st84/epistemic_governance.py --plan m45-st83-plan.json --output m45-st84-governance.json
python3 m45-st85/scientific_integrity.py --audit m45-st81-audit.json --ledger m45-st82-ledger.json --plan m45-st83-plan.json --governance m45-st84-governance.json --output m45-st85-integrity.json
```

CI generates all five artifacts with read-only repository permissions. It fails on broken integrity constraints or incomplete upstream execution evidence.

## Scope and limitations

This policy is implemented in ordinary Python and **is not technically immutable**: someone who can change the repository or CI can change these rules. SHA-256 content binding detects changes to supplied data but does not authenticate who created the data. The checker does not independently prove mathematics, validate physical hardware, or verify that the ST81 audit came from a trusted machine. It checks consistency of a supplied chain, not all possible semantic attacks or omissions. All findings remain subject to independent human review. CI status is pending.
