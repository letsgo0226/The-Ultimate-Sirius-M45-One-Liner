# M45-ST/36 — Regularized Computation: a falsifiable research proposal

This stage introduces **regularized singularity** as a *hypothesis and mathematical metaphor*, not a physical singularity or an established new theorem.

## Definition

For a finite SK computation, define the bounded observable

`O(B,L,e) = bounded_normalize(e; step_budget=B, expression_length_cap=L)`.

The regularization parameters are **finite** resource budgets `B` and `L`. The experiment increases `B` across a declared finite schedule and checks whether a normal form is *observed*. It never infers nontermination from a finite timeout. A finite budget is not the same as an analytic `epsilon → 0` limit; a true singular limit would require an independently justified topology, limit operation, and theorem.

## Run

```sh
python3 -m unittest discover -s m45-st36 -p 'test_*.py'
python3 m45-st36/regularize.py --expression '@@@SKKS'
```

The output is a deterministic, replay-checkable JSON certificate containing budgets, statuses, intermediate SK expressions and a SHA-256 digest.

## Interpretation

- `NORMAL_OBSERVED`: a normal form was reached in at least one tested finite run.
- `UNRESOLVED_WITHIN_TESTED_BUDGETS`: no normal form was observed; this does **not** mean nontermination.
- `CAP_EXCEEDED`: the resource cap blocked the next step; this is an implementation constraint, not a mathematical singularity.

The regularization operator here is a **resource-bounded observation** of an exact SK reduction, not a new semantics-preserving operator on all programs. Recursive application across an entire system is only a proposed architecture, not implemented or proven.

## Connection to previous stages

ST35 implements a finite input family with a fixed finite transition table. ST36's experimental driver deliberately uses ST32's Python reference SK reducer; it does **not** claim the ST35 machine performs general SK reduction. The next stage should study how to implement resource-bound monitoring and certified continuation at the fixed-delta TM level.

This PR is stacked on ST35 and remains unmerged until reviewed. No GitHub Actions run is confirmed.
