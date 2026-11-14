# M45-ST/50 — Micro–Macro Correspondence Operator

ST50 builds a **finite, independently prepared N-qubit model** on top of ST49's density-matrix dephasing channel. The Z-basis probability of a single qubit is `p`. A macroscopic count of Z-plus outcomes has the exact binomial distribution

`P(K=k) = C(N,k) p^k (1-p)^(N-k)`.

A coarse-graining map classifies the count into **majority plus**, **majority minus**, or **tie**. It reports mean, variance, and standard deviation of the observed fraction, which scales as `sqrt(p(1-p)/N)` under the stated independence assumption.

```sh
python3 -m unittest discover -s m45-st50 -p 'test_*.py'
python3 m45-st50/micro_macro.py --n 100 --p 0.7 --gamma 0
```

**Important scientific boundary:** ST49 dephasing is in the Z basis and does **not** change Z populations, so the macro Z count distribution remains unchanged when gamma varies. The X-basis statistics and off-diagonal coherence do change. This is an instructive difference between **measurement context**, **decoherence**, and **coarse-graining**; none of them alone proves objective collapse or creates a macro universe.

The model assumes independent, identically prepared qubits, not an interacting many-body universe. It does not simulate a physical detector or generate physical particles. No astrophysical measurements are acquired. The GitHub Actions workflow only runs read-only tests and a deterministic example. ST47 state integration remains separate and unimplemented.
