# M45-ST/77 — Relational Quantum Scientific Falsifiability and Model Criticism

ST76 chooses between symmetric and asymmetric readout models by Bayesian evidence. ST77 asks a different question: **does the posterior predictive distribution derived from the training data adequately anticipate fresh, independent measurements?**

## Design

The ST76 discrete-grid posterior is trained on three types of Bernoulli observations:

- `reference_zero`: known true zero, observed success probability `q01`.
- `reference_one`: known true one, observed success probability `1-q10`.
- `science`: relational event, observed success probability `q01+(1-q01-q10)*(1+sin(theta))/2`.

For each action, ST77 draws a **separate holdout sample**, which is not reused for model fitting. The exact finite-grid posterior predictive distribution of the holdout success count is a mixture of binomials:

`P(K=k | D_train, action)=sum_h P(h|D_train) BinomialPMF(k;n,p_h(action))`.

The diagnostic is a two-sided **posterior predictive tail area** based on distance of the holdout count from the predictive mean:

`T(k)=|k-E[K|D_train]|`, `tail=sum_{j:T(j)>=T(k_obs)} P(K=j|D_train)`.

For exploratory display, the program flags a tail area below `alpha/3` for one of the three actions. This threshold is a heuristic screening convention, **not a valid frequentist familywise error guarantee**. Bayesian posterior predictive tail areas are not generally uniform under repeated sampling with fixed true parameters.

## Model-misspecification experiment

An optional `--science-drift` adds a fixed probability shift to the **holdout science stream only**, clipped to [0,1], while training uses the original stationary detector model. This creates an explicit nonstationary alternative, allowing the diagnostic to be tested for sensitivity to out-of-model data. A flag is evidence of a predictive mismatch under this check, not a proof that every candidate model is false; absence of a flag does not establish adequacy.

```sh
python3 -m unittest discover -s m45-st77 -p 'test_*.py'
python3 m45-st77/predictive_criticism.py --train-shots 40 --holdout-shots 30 --science-drift 0.3
```

## Limits

The 1100-point grid is coarse; predictive failure may arise from discretization, prior choice, finite training data, sampling variation, or real model mismatch. A single heldout count per action has limited diagnostic power. There is no automatic model creation, no formal falsification theorem, no calibrated frequentist rejection rule, and no quantum hardware validation. The true phase, true detector error and injected drift are visible only to the simulator. This is a classical statistical experiment about the epistemology of model criticism, not proof of metaphysical observer independence. CI execution and review pending.
