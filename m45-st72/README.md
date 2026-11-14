# M45-ST/72 — Relational Quantum Self-Calibration and Epistemic Correction

ST71 demonstrated that an observer's incorrect detector calibration can invalidate a confidence interval, despite agreement on the underlying relational Born rule. ST72 adds **independent reference experiments** that allow each observer to estimate their own symmetric binary-flip error rate and propagate its uncertainty into the science estimate.

## Measurement protocol

The shared ST69 relational event has ideal probability `p(theta)=(1+sin(theta))/2` with `theta in (-pi/2,pi/2)`. Observer `i` has a true detector flip rate `q_i<1/2`.

1. **Calibration:** prepare a known binary reference outcome `0` and measure it `n_cal` times. The rate of erroneous `1` outcomes estimates `q_i`.
2. **Science:** measure the relational event independently `n_sci` times. The observed success rate estimates `r_i=q_i+(1-2q_i)p(theta)`.
3. **Correction:** invert the two estimates using `p=(r-q)/(1-2q)`, clipping to [0,1], then `theta=asin(2p-1)`. If the calibration point estimate is `qhat>=1/2`, the point estimate is undefined.
4. **Uncertainty:** for `m` observers, there are `2m` independent Bernoulli concentration events (calibration and science). Apply Hoeffding and a union bound with radii `eps_cal=sqrt(log(4m/alpha)/(2 n_cal))` and `eps_sci=sqrt(log(4m/alpha)/(2 n_sci))`. Invert the rectangle of raw-probability and calibration-rate intervals by evaluating its four corners. If the calibration interval reaches `1/2`, conservatively return the entire physical `p in [0,1]` interval.
5. **Consensus:** intersect the observer-wise theta intervals, report their intersection if nonempty, and compare against ST71-style intervals built from the old assumed calibrations.

Under correct independent Bernoulli sampling, known reference outcomes, a stable symmetric detector flip model, and common ideal Born probability, the probability that **all calibrated intervals simultaneously cover the fixed true theta** is at least `1-alpha`. This does not guarantee that a particular sample will cover it, that a point estimate is unbiased, or that any given interval intersection is nonempty.

```sh
python3 -m unittest discover -s m45-st72 -p 'test_*.py'
python3 m45-st72/self_calibration.py --theta 0.3 --calibration-shots 2000 --science-shots 2000
```

The default example deliberately includes a miscalibrated third observer: actual flip rates `0.02,0.08,0.15,0.04` and prior assumptions `0.02,0.08,0.02,0.04`. The simulator knows true rates only to generate outcomes and report diagnostics; inference uses the observed reference data.

**Limits:** a correctly known reference bit, stable detector behavior across calibration and science, independent measurements, symmetric binary errors, and a single identifiable phase parameter are assumed. The program does not prove that a detector is stable, discover its error model without reference standards, learn quantum theory from data, or establish a physical/metaphysical claim about observer-independent reality. Pseudorandom simulation only. CI execution and review pending.
