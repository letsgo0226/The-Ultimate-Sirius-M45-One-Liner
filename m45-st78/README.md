# M45-ST/78 — Relational Quantum Open-World Model Discovery (bounded prototype)

ST77 introduced independent posterior predictive checks. ST78 tests whether a **predeclared expanded hypothesis family** can outperform a stationary model on independent data, without letting a model win merely because it was selected on the same evaluation set.

## Competing candidates

Both families use the ST69 relational probability `p(theta)=(1+sin(theta))/2`, asymmetric detector errors `q01` and `q10`, and the three actions `reference_zero`, `reference_one`, `science`.

- **Stationary** (125 hypotheses): science success probability `r=q01+(1-q01-q10)*p` in both early and late phases.
- **Science drift** (625 hypotheses): the same early probability, but the late science probability becomes `clip(r+delta,0,1)`, with `delta` from a fixed five-value grid. Reference probabilities do not drift.

Each family has a uniform prior over its own finite hypothesis grid. Model comparison uses **posterior predictive log scores**, not raw maximized training likelihood. The candidate families and grids are specified before sampling.

## Three independent data splits

1. **Training** updates the discrete-grid posterior for each candidate family.
2. **Validation** compares the candidates' frozen-posterior predictive mean log scores and selects one family.
3. **Locked test** independently reports both families' scores and the selected family's score, without reselecting the winner.

Within a dataset, early and late measurements of all three action types are generated as independent Bernoulli counts. The predictive score is the **mean per-observation log score** under the posterior-averaged Bernoulli probability for each action/phase. This is a valid marginal predictive scoring convention, but it is **not** the joint posterior predictive log probability for a correlated batch under shared latent parameters. Because the drift family contains the stationary case, finite samples may prefer either family.

```sh
python3 -m unittest discover -s m45-st78 -p 'test_*.py'
python3 m45-st78/model_expansion.py --theta 0.3 --q01 0.05 --q10 0.2 --drift 0.3 --shots 30
```

**Limits:** this is *bounded candidate expansion*, not open-ended autonomous model invention. The finite grids may exclude true parameters, the injected drift is known only to the simulator, and one locked test is not a formal significance guarantee. The test set must not be reused for iterative model design. No quantum hardware, universal scientific discovery, or metaphysical proof is claimed. CI and review pending.
