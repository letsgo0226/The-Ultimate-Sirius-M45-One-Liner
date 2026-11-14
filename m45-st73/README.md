# M45-ST/73 — Relational Quantum Epistemic Learning and Adaptive Experiment Design

ST72 used fixed numbers of known-reference detector calibration trials and quantum science trials. ST73 adds a sequential **adaptive resource-allocation controller** that chooses which experiment to run next, subject to a fixed trial budget and a target confidence-interval width.

## Model and adaptive protocol

The finite-Z2 relational quantum model from ST69 has ideal binary probability `p(theta)=(1+sin(theta))/2`. A symmetric detector flip rate `q<1/2` gives observed science probability `r=q+(1-2q)p(theta)`. A separate known-zero reference stream produces calibration-error observations with Bernoulli probability `q`.

1. Start with `batch` calibration and `batch` science observations.
2. Estimate `q` and `r` independently from their own streams.
3. Choose the next batch by comparing first-order sensitivity-weighted predicted reductions of the Hoeffding radii: calibration sensitivity `|2rhat-1|/(1-2qhat)` versus science sensitivity `1`, with each stream's `1/sqrt(n)-1/sqrt(n+1)` improvement. This is a **heuristic**, not a proven globally optimal policy.
4. Compute a conservative confidence interval for `theta` by inverting the rectangle of calibration/science probability intervals, using all four corners; if the calibration interval reaches `q=1/2`, report the full `[-pi/2,pi/2]` interval.
5. Stop if the interval width reaches the target, or the total trial budget is exhausted. The program reports the complete look-by-look history.

## Valid coverage under adaptive stopping

A confidence interval calibrated for one pre-fixed sample size may fail under repeated optional stopping. To avoid that error, this implementation pre-allocates a union-bound budget over **all possible looks and both Bernoulli streams**, with conservative radius

`epsilon(n)=sqrt(log(4*budget/alpha)/(2*n))`.

For each stream, its first `n` observations form an i.i.d. Bernoulli prefix even if the controller adaptively chooses which stream to sample next. A union bound over all `n<=budget` and both streams therefore guarantees **simultaneous coverage at least `1-alpha`**, under the stated model. This also covers data-dependent stopping and adaptive allocation. The guarantee is conservative and is not an optimization guarantee.

```sh
python3 -m unittest discover -s m45-st73 -p 'test_*.py'
python3 m45-st73/adaptive_design.py --theta 0.3 --flip 0.15 --budget 4000 --batch 100 --target-width 0.35
```

**Limitations:** a known-zero reference source, independent and stable Bernoulli streams, symmetric stationary detector noise, one identifiable parameter `theta in (-pi/2,pi/2)`, and the correct ST69 Born model are assumed. This is seeded classical simulation, not a quantum hardware experiment. The controller has no proof of optimality, and stopping early is not guaranteed. The parameter, true detector error, and coverage diagnostics are visible only to the simulator. The model does not demonstrate autonomous scientific discovery or metaphysical observer-independent reality. Read-only CI; workflow execution and review pending.
