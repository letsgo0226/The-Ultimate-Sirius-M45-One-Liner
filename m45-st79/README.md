# M45-ST/79 — Relational Quantum Scientific Model Evolution

ST78 compared a stationary model with a late-science-drift extension. ST79 implements **bounded, traceable candidate mutation**: a finite mutation grammar proposes changes to the late-phase response of exactly one of three measurement actions.

## Candidate grammar

All candidates share a latent relational Born probability `p(theta)=(1+sin(theta))/2`, a false-positive rate `q01`, and a false-negative rate `q10`. They differ only in a predeclared late-phase additive drift:

- `stationary`: no late drift, 125 grid points.
- `science_drift`: late science response shifted, 625 grid points.
- `reference_zero_drift`: late known-zero reference response shifted, 625 grid points.
- `reference_one_drift`: late known-one reference response shifted, 625 grid points.

Each drift parameter takes one of `[-0.3,-0.15,0,0.15,0.3]`; each grid probability is bounded to [1e-12,1-1e-12] for numerical stability. This is **not open-ended program synthesis**. No candidate executes generated code.

## Auditable selection protocol

1. Independent training measurements fit a uniform finite-grid posterior for each candidate.
2. Independent validation measurements score the frozen posterior predictive means. A declared small complexity penalty applies to drift families.
3. The candidate with the largest validation score is selected, and every candidate's grid size, raw score, penalty, final score and selection flag is recorded in an audit trail.
4. A separate **locked test** scores **only the already-selected candidate**. It never feeds back into candidate generation or selection.

Predictive scoring is the average marginal Bernoulli log score per observation, not a joint batch evidence score. The complexity penalty is a declared heuristic, not an information criterion with proven optimality.

```sh
python3 -m unittest discover -s m45-st79 -p 'test_*.py'
python3 m45-st79/model_evolution.py --shots 30 --late-science-drift 0.3
```

## Scientific limits

Candidate families are manually predefined; this is a controlled model-selection experiment, not autonomous discovery of new physical laws. Results are sensitive to prior grid resolution, random seed, penalty choice and sample size. The locked test is a single independent evaluation, not a calibrated significance test or proof of the selected model. Reusing that test to tune later versions would invalidate its locked status. No physical quantum hardware or metaphysical theorem is demonstrated. CI and code review pending.
