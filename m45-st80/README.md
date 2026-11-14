# M45-ST/80 — Relational Quantum Scientific Discovery Benchmark

ST79 introduced bounded, auditable model mutation with separate training, validation and locked test splits. ST80 evaluates whether the validation-selected evolving model predicts **independent held-out data** better than the fixed stationary baseline, across repeated simulation seeds and several predeclared scenarios.

## Four simulated scenarios

- `stationary`: no late science drift.
- `positive_science_drift`: +0.30 late science response shift.
- `negative_science_drift`: -0.30 late science response shift.
- `off_grid_science_drift`: +0.22 late science response shift, deliberately between candidate grid values.

The true detector parameters and relational Born probability are fixed across scenarios. Each scenario runs independent replicates with **three separate random data splits**. Each replicate fits all four ST79 candidate families on training data, selects a family using validation predictive log score minus a predeclared complexity penalty, then evaluates the selected model and the stationary baseline on the **same locked test dataset**. The locked test is never used to choose a candidate.

## Outcomes and interpretation

The primary outcome is the **paired per-observation locked-test predictive log-score gain**:

`gain_i = score(selected_i, test_i) - score(stationary_i, test_i)`.

A positive gain means the evolving model better predicted that replicate's locked test; negative gain means the fixed model did better. Each scenario reports mean scores, the paired gain mean and sample SD, a normal-approximation 95% interval for mean gain, win fraction, selection frequencies, and per-replicate results.

The normal-approximation interval is **descriptive** and may be unreliable with small samples, skewness, or dependence. The program does not perform a preregistered significance test or control familywise error across scenarios. An interval excluding zero is not, by itself, a discovery claim.

```sh
python3 -m unittest discover -s m45-st80 -p 'test_*.py'
python3 m45-st80/discovery_benchmark.py --replicates 12 --shots 20 --seed 2026
```

## Limitations

The mutation grammar is manually defined and bounded; no open-ended hypothesis synthesis occurs. The simulator is classical and uses the same broad model family for data generation and fitting except for off-grid parameters. Candidate grids, priors, sample size, penalties and seeds affect results. The per-observation predictive log score uses marginal posterior-averaged Bernoulli probabilities, not the full joint posterior predictive likelihood for a batch. Repeatedly inspecting the same locked test for further development would compromise its independence. ST80 does not establish quantum hardware behavior, a new physical law, or autonomous scientific discovery. CI and review pending.
