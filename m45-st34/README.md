# M45-ST/34 — Atomic K rule on a fixed-delta single-tape TM

This stage generalizes ST33's **one exact K redex** to **all four atomic cases** of `Kxy → x` where `x,y ∈ {S,K}`. Each computation is defined by the same fixed, finite transition table `delta.json` (no generated per-input table).

Supported complete expressions:
- `@@KSS → S`
- `@@KSK → S`
- `@@KKS → K`
- `@@KKK → K`

The table checks the full input and blank end marker, remembers `x` in its finite control state, erases the other four cells and writes `x` into the first tape cell. A generic Python simulator executes one table transition per TM step; it does not perform SK rewriting itself.

## Run locally

```sh
python3 -m unittest discover -s m45-st34 -p 'test_*.py'
python3 m45-st34/tm.py --expression '@@KSK'
```

## Research boundaries

This is **not yet the general K rule**: `x` and `y` must each be exactly one atomic symbol. Arbitrarily nested SK subexpressions require explicit parsing, boundary finding and copying on the tape with finite control, which is future work. It is not a universal TM, a general SK normalizer, or an implementation of the S rule.

A GitHub Actions workflow runs tests and uploads a trace artifact, but no workflow execution or live deployment is claimed. The branch is stacked on ST33, which depends on ST32/ST31/ST30/ST29/ST28. Review and merge in dependency order.
