# M45-ST/37 — Exact-by-Construction SK Verification

## Invariant

Resource regularization must **never silently approximate an SK result**. A reduction is accepted only when an independent, deterministic verifier recomputes the exact leftmost-outermost SK transition. If resources are exhausted, the result is `PAUSED` or `CAP_EXCEEDED`, not an invented normal form.

ST37 uses **symbolic syntax trees and integers**, not floating-point arithmetic. It runs ST32's SK reducer as the producer and a separate pattern-matching reducer as the verifier. A certificate includes all intermediate exact expressions, a status, and a SHA-256 digest. Even if an attacker edits the trace and recomputes the digest, a mathematically invalid step is rejected by the independent verifier.

## Run

```sh
python3 -m unittest discover -s m45-st37 -p 'test_*.py'
python3 m45-st37/exact.py --expression '@@@SKKS' --budget 30 --cap 300
```

The verifier's input is limited to 300 prefix symbols, a budget of at most 100 steps, and a maximum expression length of 300 symbols. These are explicit **resource restrictions**, not numerical approximation. `NORMAL` means the exact reducer finds no further step in this specified strategy. `PAUSED` means budget exhaustion, not nontermination. `CAP_EXCEEDED` means the input or next step exceeds the declared length limit.

## Important limits

- Two Python implementations agreeing is stronger evidence than one, but **not** a formal proof of correctness of Python, the runtime, the hardware, or all possible programs.
- SHA-256 is an integrity digest, not an authenticity signature. Verification requires trusted code and input.
- This module is a reference-level exact SK evaluator and verifier, **not** a general fixed-transition-table SK Turing machine. ST35 remains a finite-domain fixed-delta demonstration.
- A recursive system-wide regularizer remains future work; this PR implements a verified computation boundary only.
- GitHub Actions workflow is defined but no online run, merge or deployment has been confirmed.

The next stage should extend the exact verification contract to persistent journals and fixed-delta TM traces.
