# M45-ST/38 — Verified Persistent Computation

A local JSON ledger makes exact SK reduction **resumable and independently replay-verifiable**. Each batch is produced by ST37, checked by its independent symbolic SK verifier, and linked to the preceding batch by a SHA-256 digest. The ledger itself is checked before and after each update.

## Commands

```sh
python3 -m unittest discover -s m45-st38 -p 'test_*.py'
python3 m45-st38/ledger.py --file ledger.json --init --expression '@@@SKKS' --budget 1
python3 m45-st38/ledger.py --file ledger.json --budget 1
python3 m45-st38/ledger.py --file ledger.json --verify-only
```

The two batches perform `@@@SKKS → @@KS@KS → S`. After `NORMAL` or `CAP_EXCEEDED`, continuation is refused. A resource cap is not an approximation: no result is asserted unless all recorded steps pass the independent verifier.

## Persistence and trust boundaries

- The ledger is stored in **one JSON file**, updated via a temporary file, `fsync`, and atomic replacement on supported local filesystems. This avoids mismatched state/journal files; it is not a guarantee against all power-loss or storage-device failures.
- The sequence is logically append-only, but physically the JSON file is **rewritten** on each update. A privileged actor can replace or truncate the entire file. A SHA-256 chain is **not** a signature or external trusted timestamp.
- The verifier recomputes each exact SK transition using ST37's independent implementation. This is stronger than hash-only verification, but not a formal proof of Python, hardware or operating-system correctness.
- The runner is **not** a general fixed-delta TM. ST35 is a separate finite-input fixed-table TM; ST38 resumes the ST37 reference SK evaluator.
- This GitHub Actions workflow is **read-only** and uploads a ledger artifact; it does not commit state to the repository or run continuously. No online run or merge has yet been confirmed.

## Next research milestone

A formally specified, canonical ledger format with external checkpoint anchoring and a general fixed-delta SK machine could make the persistence and execution claims substantially stronger.
