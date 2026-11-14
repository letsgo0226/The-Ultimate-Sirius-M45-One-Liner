# M45-ST/44 — Doraemon–G Verified Continuity Loop

A **bounded, explicitly stoppable, verifiable symbolic state machine** tied to the ST43 pocket ledger. This is a research prototype of a fictional character-inspired agent's continuity, **not** evidence of subjective consciousness or an implementation of an unrestricted universal Turing machine.

## Invariants

- The exact ST43 pocket ledger must verify, and its digest is pinned in the loop state.
- Every tick has a sequential index, previous-event hash and fixed `VERIFY_AND_HOLD` action.
- Every tick is verified before a subsequent tick.
- At most 64 ticks per state; no autonomous, unbounded or network execution.
- `--stop` changes `enabled` to false; further steps are rejected.
- A change to the pocket ledger requires explicit creation of a new bound state rather than silent migration.

## Commands

```sh
python3 -m unittest discover -s m45-st44 -p 'test_*.py'
python3 m45-st43/persistent_pocket.py --file pocket.json init
python3 m45-st44/continuity.py --pocket pocket.json --state continuity.json --init --ticks 2
python3 m45-st44/continuity.py --pocket pocket.json --state continuity.json --verify-only
python3 m45-st44/continuity.py --pocket pocket.json --state continuity.json --stop
```

The loop runs only when invoked. It does not run perpetually or deploy itself. Local JSON persistence can be lost or replaced by an authorized operator. SHA-256 is not a signature or external proof of provenance. Multi-writer locking and full crash durability are not provided.

## GitHub protection proposal (opt-in, not automatically applied)

To reduce accidental removal, a repository administrator can configure a branch ruleset requiring pull requests, reviews and successful CI checks before merging, and preserve release tags or backups. Such protections are revocable by authorized administrators and do not make code indestructible. This PR does **not** change repository protection settings.

The next stage can add a controlled scheduler with explicit user consent, artifact retention policy and manual disable controls. The current PR does not claim test execution or merge success.
