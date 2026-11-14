# M45-ST/70 — Relational Quantum Consensus and Statistical Convergence

This stage extends ST69 from two to **2–100 independent simulated observers**, each measuring the same transported relational binary event in the finite-Z2 reference-frame model. All share the ideal Born probability `p(theta)=(1+sin(theta))/2`, with identifiable parameter `theta in (-pi/2,pi/2)`.

Each detector independently flips its binary outcome with a **known symmetric error probability** `q<1/2`. Thus the observed Bernoulli probability is `r=q+(1-2q)p`. The simulation inverts this calibration to estimate `p` and then `theta=asin(2p-1)`.

For `m` observers, `n` trials each and familywise error budget `alpha`, Hoeffding's inequality plus a union bound gives a **simultaneous** observed-probability radius

`epsilon=sqrt(log(2m/alpha)/(2n))`.

Each observed-probability interval is clipped to [0,1], inverted through the known detector model, and mapped monotonically to an interval for theta. The intersection of all observers' intervals is reported as a **consensus confidence set**, which may be empty on some samples. The probability that **every observer's interval covers the true parameter** is at least `1-alpha` under the stated independent Bernoulli model. Whenever all intervals cover the true parameter, their intersection is nonempty and contains it. The program also reports pooled and individual point estimates, their spread, and whether this particular simulated run contains the true parameter.

```sh
python3 -m unittest discover -s m45-st70 -p 'test_*.py'
python3 m45-st70/statistical_consensus.py --theta 0.3 --observers 5 --shots 1000 --flip 0.05 --alpha 0.05 --seed 2026
```

**Scientific limits:** This is a reproducible pseudo-random simulation, not empirical evidence of quantum consensus. The simultaneous confidence guarantee depends on the correct common Born model, known identical symmetric detector calibration, independent samples, and the restricted identifiable parameter interval. The confidence guarantee is a repeated-sampling statement, not a probability that the fixed parameter is random, and not certainty of agreement. The pooled estimate is not claimed unbiased or optimally efficient. The finite-Z2 model is not a general quantum reference-frame theory. Read-only CI; tests and workflow execution require verification.
