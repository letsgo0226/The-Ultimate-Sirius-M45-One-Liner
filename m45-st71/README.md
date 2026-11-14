# M45-ST/71 — Relational Quantum Consensus Under Model Disagreement

ST70 assumed that every observer knew the correct symmetric detector-flip probability. ST71 tests the consequences of relaxing that assumption.

All observers still share the same **ideal** relational Born probability `p(theta)=(1+sin(theta))/2` in the ST69 finite-Z2 model. Observer `i` has a true detector flip probability `q_i` and an **assumed** calibration `qhat_i`. Simulated binary observations have probability `r_i=q_i+(1-2q_i)p`. The observer instead estimates `p` using `(rhat_i-qhat_i)/(1-2qhat_i)`, clipped to [0,1], and maps it to `theta=asin(2p-1)`.

For `m` observers with `n` independent samples each, simultaneous Hoeffding intervals for **raw observed** probabilities use `epsilon=sqrt(log(2m/alpha)/(2n))`. Inverting them through the **assumed** calibration yields assumption-based confidence intervals. For comparison only, the simulator also computes **oracle** intervals using the actual calibration rates, which a real observer would not automatically know.

**Critical distinction:** The union-bound simultaneous coverage guarantee `>=1-alpha` applies to the oracle intervals (and to assumption-based intervals only when all calibrations are correct). It does **not** apply to misspecified intervals, even if their intersection is nonempty. An interval intersection is not proof of the model's correctness. Differences in individual estimates can reflect sampling noise, calibration bias, or both.

Default configuration: four observers with actual flips `0.02,0.08,0.15,0.04` but assumed flips `0.02,0.08,0.02,0.04`. This deliberately makes observer 3 miscalibrated.

```sh
python3 -m unittest discover -s m45-st71 -p 'test_*.py'
python3 m45-st71/model_disagreement.py --theta 0.3 --shots 1000 \
  --actual-flips 0.02,0.08,0.15,0.04 --assumed-flips 0.02,0.08,0.02,0.04
```

**Scope:** Known true calibration is used by the simulator to generate outcomes and oracle comparisons, not learned from data. Calibration bias is not identifiable from a single binary probability without additional assumptions or reference standards. This stage does not implement a reliable automatic model-selection test, Bayesian prior disagreement, or experimental quantum devices. It is a finite-Z2, independent Bernoulli simulation with pseudo-random samples. Read-only CI; tests and workflow execution await verification.
