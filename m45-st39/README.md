# M45-ST/39 — Verified Bounded Controller

ST39 is a **finite feedback controller** around ST38's persistent ledger and ST37's independently verified exact SK reduction. It checks the existing ledger, applies a deterministic resource policy, performs at most one verified batch at a time, atomically persists it, reloads and verifies it, then repeats until normal form, a resource limit, or an error.

This is a testable engineering interpretation of *recursive regularization*: feedback is applied to the **controller's execution loop**. It is not a mathematical singularity, self-modifying universal computer, halting oracle, or proof of infinite convergence.

## Exactness contract

1. Every accepted SK step must satisfy the independent ST37 symbolic semantics.
2. A resource limit **stops or pauses** computation; it never substitutes an approximate answer.
3. Every persisted batch is semantically verified before and after the update.
4. Invalid state blocks execution (fail closed).
5. Policy is bounded by finite integers: maximum batches, steps per batch, and cumulative steps.

## Run

```sh
python3 -m unittest discover -s m45-st39 -p 'test_*.py'
python3 m45-st39/controller.py --init --file ledger.json --expression '@@@SKKS' --max-batches 8 --steps-per-batch 1 --max-total-steps 32
python3 m45-st39/controller.py --verify-only --file ledger.json
```

The default example normalizes in two verified batches, yielding `S`. An already-existing ledger is never overwritten by `--init`.

## Limits

- The controller uses ST37/ST38's Python symbolic reference implementation, not a general fixed-transition-table SK Turing machine.
- SHA-256 detects accidental or unsophisticated tampering; it is not a signature, trusted timestamp or defense against a malicious actor replacing the whole ledger and verifier.
- Atomic file replacement does not guarantee survival of all hardware failures, nor provide multi-writer locking. **Do not run concurrent writers on the same ledger.**
- GitHub Actions is a read-only test and artifact workflow; no automated production deployment, merge, or verified online run is claimed.
- The resource policy is fixed at launch and is not autonomously optimized or self-modified.

A future stage can introduce formally specified ledger schemas, authenticated checkpoints, and concurrency control.
