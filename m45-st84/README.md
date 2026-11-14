# M45-ST/84 — Relational Quantum Epistemic Governance

ST83 produces advisory-only recommendations from gaps in the ST82 evidence ledger. ST84 introduces a **fail-closed, read-only governance gate** that classifies those recommendations by predefined review risk, binds each decision to the original task hash, and requires independent review before any future implementation.

## Rules

Only the seven explicitly allowlisted ST83 actions are recognized. The input plan must have the expected protocol and advisory-only policy; each task must state `requires_human_approval=true` and `auto_execute=false`. A task whose action conflicts with its failed evidence check is rejected. Duplicate tasks and contradictory scientific-truth claims are rejected.

Risk categories and review requirements:

- **High**: execution failure, nondeterminism, missing source, failed unit tests; independent reviewer required.
- **Medium**: source hash mismatch or missing output digest; maintainer review required.
- **Low**: missing ST81 audit; maintainer review required.

Every decision is `PENDING_HUMAN_REVIEW`, `approved=false`, `execution_permitted=false`. High/medium actions flag a rollback plan as required if ever implemented. Required future evidence includes review record, fresh unit tests, fresh ST81/ST82 audit and a separate implementation PR.

```sh
python3 -m unittest discover -s m45-st84 -p 'test_*.py'
python3 m45-st81/reproducibility_audit.py --run-tests --output m45-st81-audit.json
python3 m45-st82/evidence_ledger.py --audit m45-st81-audit.json --output m45-st82-ledger.json
python3 m45-st83/epistemic_correction.py --ledger m45-st82-ledger.json --output m45-st83-plan.json
python3 m45-st84/epistemic_governance.py --plan m45-st83-plan.json --output m45-st84-governance.json
```

CI runs with read-only repository permissions and uploads the four JSON artifacts; it cannot approve changes, execute repair proposals or deploy code. It checks upstream evidence and fails if required audit evidence is incomplete.

## Scientific and security limits

Risk levels are **policy heuristics**, not calibrated probabilities of harm. The task and plan hashes bind decisions to their input content but do not provide authentication or tamper-proof provenance. This stage does not validate quantum physics, establish a metaphysical theorem, create a general-purpose self-modifying AI or replace human oversight. The governance artifact is a review queue, not an authorization token. CI and independent review pending.
