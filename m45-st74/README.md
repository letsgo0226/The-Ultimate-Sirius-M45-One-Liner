# M45-ST/74 — Relational Quantum Active Learning and Experimental Optimization

ST73 introduced a sensitivity-based adaptive controller for deciding whether to perform a known-reference detector calibration or a relational quantum science measurement. ST74 supplies a **reproducible paired Monte Carlo benchmark** to compare this controller with fixed allocation policies under the same finite trial budget.

## Policies

- **Balanced:** assign the next batch to the stream with fewer observations.
- **Science-heavy:** preferentially allocate science measurements until their sample count is about three times calibration.
- **Adaptive:** reuse ST73's sensitivity-weighted marginal reduction heuristic.

All policies begin with one batch in each stream, then stop when their propagated theta interval reaches a common target width or the budget is exhausted. Each replicate draws two independent Bernoulli sequences, one for calibration and one for science; **all policies consume prefixes of the same two sequences** within that replicate. This paired common-random-numbers design reduces extraneous Monte Carlo variation when comparing policies.

The true detector flip probability `q` is unknown to the inference policy, but known to the simulator. A reference outcome of 0 provides Bernoulli calibration errors with probability `q`. Science success probability is `r=q+(1-2q)*(1+sin(theta))/2`. The corrected estimator inverts this relation, with `theta in (-pi/2,pi/2)`.

## Coverage and metrics

The ST73 simultaneous confidence interval uses the conservative radius `sqrt(log(4*budget/alpha)/(2*n))` for both streams across all potential looks, retaining a per-replication coverage lower bound `1-alpha` under adaptive allocation and optional stopping. The benchmark reports empirical coverage (which can fluctuate), mean interval width, target-hit fraction, mean trial usage, calibration/science split, estimator bias, RMSE, and paired mean differences versus balanced allocation.

**Important:** A finite Monte Carlo comparison does not prove any policy globally optimal. No significance test or confidence interval for between-policy performance is supplied. Lower observed RMSE in one seed is not proof of superiority. Coverage claims rely on independent stable Bernoulli streams, a correct symmetric detector model, known-zero reference outcomes, and the finite-Z2 relational Born model. The benchmark is classical simulation, not physical quantum hardware. Policy CPU time is not benchmarked, and an actual information-gain optimizer is not implemented in this stage.

```sh
python3 -m unittest discover -s m45-st74 -p 'test_*.py'
python3 m45-st74/active_learning_benchmark.py --theta 0.3 --flip 0.15 --budget 1200 --batch 50 --replications 100 --target-width 0.65
```

Read-only CI; execution and review pending.
