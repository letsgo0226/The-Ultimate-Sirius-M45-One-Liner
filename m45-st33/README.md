# M45-ST/33 — A real fixed-delta single-tape SK K-redex demonstrator

This is the first deliberately **narrow** SK reduction in this research series implemented using only a fixed, finite transition table. The table in `delta.json` recognizes the **exact complete expression** `@@KSK` (i.e., `K S K`) and rewrites the tape to `S`. There are 11 TM transitions. Each transition reads one cell, writes one symbol, and moves its head L/R/N. No Python SK parser or reduction function is used to determine the next TM transition.

```sh
python3 -m unittest discover -s m45-st33 -p 'test_*.py'
python3 m45-st33/tm.py --expression '@@KSK'
```

The certificate contains the explicit step trace and the transition-table SHA-256 digest. The verifier replays the deterministic machine from the original input and checks exact equality.

## Essential limitations

- This machine accepts **only** the exact five-symbol input `@@KSK`. It is a fixed-delta *example* of the K rule, **not a general K-reducer, S-reducer, universal SK interpreter, or universal Turing machine**.
- It does not yet implement ST32's general tape encoding (which uses numeric cells) or support arbitrary SK syntax.
- The runner's Python implementation is a generic finite transition executor, not an SK reducer; the transition table itself defines the operation.
- GitHub Actions runs finite jobs; the PR has not been merged or run online.
- This branch depends on ST32, ST31, ST30, ST29, ST28 in order.

## Next formal milestone

ST34: generalize K redex recognition to arbitrary well-formed subterms using a finite tape alphabet and explicit machine states, then test equivalence with ST32 on bounded inputs. The S rule and a full normalizer would remain later milestones.
