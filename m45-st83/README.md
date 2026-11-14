# M45-ST/83 — Relational Quantum Epistemic Self-Correction

This is a **read-only, advisory-only** planner for prioritizing evidence repair tasks. It consumes the source-bound ST82 evidence ledger (itself based on the ST81 audit) and suggests the next verification step for each unverified stage. It does not edit source files, run suggested commands, approve PRs, or deploy anything.

## Decision policy

For each unverified claim, examine ST82 checks in dependency order: source present, audit present, successful execution, matching source hash, output digest present, deterministic repeat, and unit tests passed. Suggest **only the earliest failed prerequisite** to avoid cascades of speculative downstream repair work. Prioritize nondeterminism and failed execution, then missing source, failed tests, mismatched hashes, missing audit and missing digests. Deterministic tie-breaking uses stage name. A task cap prevents unbounded output.

The output contains action, priority, failed check, stage, source path, reason and explicit `requires_human_approval=true`, `auto_execute=false`. No suggestions are treated as executed. `AUDIT_VERIFIED` is not interpreted as scientific truth.

## Usage

```sh
python3 -m unittest discover -s m45-st83 -p 'test_*.py'
python3 m45-st81/reproducibility_audit.py --run-tests --output m45-st81-audit.json
python3 m45-st82/evidence_ledger.py --audit m45-st81-audit.json --output m45-st82-ledger.json
python3 m45-st83/epistemic_correction.py --ledger m45-st82-ledger.json --output m45-st83-plan.json
```

The read-only GitHub Actions workflow produces and uploads all three JSON artifacts even if the upstream audit detects failures, then enforces a full ST82 audit coverage check. The planner does not conceal failed verification.

## Limits

This is a rule-based diagnostic scheduler, not an autonomous theorem prover, agentic code editor, or validated scientific discovery system. The ST82 ledger is trusted as input; ST83 validates its structure and rejects contradictory verified entries, but it does not independently authenticate the provenance of the ledger or its underlying audit. A passing unit test is evidence of software behavior, not a physical theory. No self-modifying code or automatic deployment is implemented. CI and independent review pending.
