# M45-ST/76 — Relational Quantum Bayesian Experimental Design and Model Selection

ST75 optimized an approximate phase-estimation risk under an assumed symmetric readout model. ST76 explicitly considers **two competing detector models** and selects experiments by the **exact one-step expected information gain about the model indicator** under a finite discrete Bayesian grid.

## Competing readout models

The ST69 relational binary event has ideal probability `p(theta)=(1+sin(theta))/2` with `theta in (-pi/2,pi/2)`. A detector can make two distinct errors:

- `q01 = P(observe 1 | true 0)`
- `q10 = P(observe 0 | true 1)`

The competing models are:

- **Symmetric:** `q01=q10=q`.
- **Asymmetric:** `q01` and `q10` are independently parameterized (the grid includes the symmetric subspace).

Available experiment actions:

1. `reference_zero`: known true 0; probability of observed 1 is `q01`.
2. `reference_one`: known true 1; probability of observed 1 is `1-q10`.
3. `science`: relational event; probability of observed 1 is `q01+(1-q01-q10)*p(theta)`.

The program enumerates a fixed **1100-hypothesis discrete grid**: ten phase probabilities and ten symmetric rates, or ten phase probabilities and 100 ordered asymmetric rate pairs. It uses uniform mass within each model and an explicit prior model probability (default 0.5). The evidence calculation uses log likelihoods and log-sum-exp normalization; the asymmetric model is not automatically rewarded merely for having more grid points.

## Active Bayesian design

For each available action, compute its model-averaged Bernoulli predictive probability and the model-specific predictive probabilities. The **exact finite-grid one-step model-information gain** is

`I(M;Y|D,a)=H(Y|D,a)-sum_m P(m|D) H(Y|M=m,D,a)`,

where `H` is binary entropy in nats. Choose the action with the largest expected model information, simulate one outcome, update the posterior, and repeat. The program reports a posterior probability for each model, the action-level information gains, selected actions, and the model-averaged posterior mean phase estimate.

```sh
python3 -m unittest discover -s m45-st76 -p 'test_*.py'
python3 m45-st76/bayesian_model_selection.py --theta 0.3 --q01 0.05 --q10 0.2 --steps 12
```

## Scientific and statistical limitations

The true detector rates and true phase are used only to generate simulation outcomes and annotate diagnostics. The grid is deliberately coarse and finite; the true parameters may be off-grid, causing discretization bias. Bayesian model probabilities depend on the chosen priors and hypothesis grid. The asymmetric model contains symmetric settings; this is a finite model-comparison exercise, not a guarantee of identifying the true model. A one-step information objective is **not** a globally optimal sequential policy. Unlike ST73–ST75, ST76 does **not** claim frequentist confidence coverage for its Bayesian posterior summaries. The simulator assumes stable independent Bernoulli outcomes and correctly known reference bits. It does not demonstrate quantum hardware behavior, physical observer independence, autonomous discovery, or a general metaphysical theorem. CI and review pending.
