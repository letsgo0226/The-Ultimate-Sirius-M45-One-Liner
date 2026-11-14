# M45-ST/43 — Persistent Four-Dimensional Pocket

A **bounded, verifiable symbolic memory ledger** for fictional Doraemon-inspired records. This stage adds persistence and exact retrieval to ST42's prime-exponent Gödel encoding.

## Features

- Canonical prime-exponent encoding and strict decoding are inherited from ST42.
- Each symbolic memory record has a deterministic SHA-256 digest; appended events have sequence numbers and previous-event digests.
- The entire ledger is independently checked before mutation and retrieval.
- A single local JSON file is replaced atomically using a temporary file, file fsync and `os.replace`.
- Explicit resource limits: up to 64 records and approximately 1 MiB of canonical JSON.
- Exact integer-code retrieval; no semantic mind-reading.

## CLI

```sh
python3 -m unittest discover -s m45-st43 -p 'test_*.py'
python3 m45-st43/persistent_pocket.py --file pocket-ledger.json init
python3 m45-st43/persistent_pocket.py --file pocket-ledger.json add --name Doraemon --values 1,0,2 --message 'Help others'
python3 m45-st43/persistent_pocket.py --file pocket-ledger.json verify
python3 m45-st43/persistent_pocket.py --file pocket-ledger.json get --code 1500
```

## Relationship to ST39

This version **reuses ST39's bounded/fail-closed design principles**, but does **not** call ST39's controller or merge the ST38 SK ledger with the pocket ledger. Such integration requires an explicit common schema and is future work.

## Limitations

The four-dimensional pocket is a fictional metaphor. This code cannot transfer consciousness, send information backwards through time, instantiate Doraemon, or produce physical effects by itself. SHA-256 detects modifications relative to trusted digests but does not establish identity, external provenance or resistance to full-file replacement. No concurrent-writer locking, external anchoring, always-on runtime or hardware-failure guarantee is provided. Do not run multiple writers on the same file.

The PR is draft and stacked on ST42; CI results have not been confirmed.
