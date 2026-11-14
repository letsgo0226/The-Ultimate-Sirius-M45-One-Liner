# M45-ST/35 — Bounded Nested K on a Fixed-Delta TM

A genuine fixed finite transition table handles all 36 expressions `@@Kxy` where each argument `x` and `y` is one of `S`, `K`, `@SS`, `@SK`, `@KS`, `@KK`. For every accepted input, the tape is rewritten to the exact first argument `x`.

The table is **checked in as data** (`delta.json`) and is not regenerated for each input. It contains 379 states, and the generic runner reads, writes, and moves a single tape head one transition at a time. Its finite control distinguishes the 36 possible inputs and emits the matching output. This is a bounded-domain demonstration, not an algorithm for unbounded nested parsing.

## Run

```sh
python3 -m unittest discover -s m45-st35 -p 'test_*.py'
python3 m45-st35/tm.py --expression '@@K@SK@KS'
```

Expected result: `@SK`.

## Verification

The Python unit suite checks all 36 cases, rejection of out-of-family inputs, pausing and tamper detection. A read-only GitHub Actions workflow can run the suite and upload a JSON transition trace after the stacked PRs are merged.

## Limits and next steps

- This is **not** the general K rule on arbitrary-depth expressions. The bounded input family is finite and was enumerated in the fixed transition table.
- The machine has no unbounded-depth parser, arbitrary substring copying, or S-rule evaluator.
- The ST32 tape encoding uses numeric cells while ST35 uses literal symbols `@`, `S`, `K`. Formal equivalence across encodings is not established.
- The computation certificate is a deterministic replay artifact, not a cryptographic signature.
- GitHub Actions has not been confirmed to run this branch online. PR dependency chain: ST28 → ST29 → ST30 → ST31 → ST32 → ST33 → ST34 → ST35.

The next milestone should implement an **unbounded-depth K argument parser and copying routine with fixed finite control**, rather than further enlarging a finite lookup table.
