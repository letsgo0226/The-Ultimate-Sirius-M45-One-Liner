# M45-ST/69 — Relational Quantum Estimation and Observer Agreement

Two observers independently sample the **same transported relational binary event** in the finite-Z2 model developed in ST64 and ST68. The A-frame state is `(|00>+i|01>+|10>-i|11>)/2`; the parameter is encoded by `exp(-i theta (I tensor X)/2)`. The event `B=C` has the exact Born probability

`p(theta) = (1+sin(theta))/2`.

The B observer uses the ST64 reference switch for both the encoded state and the event. The theoretical probabilities agree exactly up to floating-point tolerance. **Independent finite-sample outcomes do not have to agree.**

For `theta` strictly between `-pi/2` and `pi/2`, the model is identifiable; the plug-in estimate is `theta_hat=asin(2 k/n-1)`. At finite-sample boundaries `k=0` and `k=n`, estimates are clipped to the parameter interval endpoints. This estimator is not claimed to be exactly unbiased.

For the selected state and event, classical Fisher information `F_C=1` equals quantum Fisher information `F_Q=1` in the interior. The reported `1/sqrt(n F_C)` is an **asymptotic standard-error benchmark**, not a guaranteed finite-sample confidence interval. Each observer receives independent seeded pseudo-random Bernoulli samples.

```sh
python3 -m unittest discover -s m45-st69 -p 'test_*.py'
python3 m45-st69/observer_estimation.py --theta 0.3 --shots 1000 --seed 2026
```

**Limits:** finite global-Z2-even sector, ideal independent samples, known state preparation and noise-free detector, a single identifiable parameter, and no actual laboratory data. Common predictions do not entail identical individual outcomes, perfect interobserver agreement, or objective ontology. Python pseudo-randomness is simulation only, not quantum randomness. Read-only CI; tests and CI pending execution.
