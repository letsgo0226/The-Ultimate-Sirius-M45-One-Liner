# Counterexample: conformal trace stationarity does not imply vacuum Einstein equations

Take `g_mu nu=Omega(t)² eta_mu nu` with signature `+---` and `Omega(t)=2+t`, on any local patch where `t>-2` so `Omega>0`.

The conformally restricted Einstein–Hilbert Euler–Lagrange equation is

```text
delta S_EH / delta Omega = -12 Box_eta Omega = 0.
```

Since Omega is linear, `Box_eta Omega=0`; therefore `R=-6 Omega^-3 Box_eta Omega=0`. However, the Einstein tensor remains nonzero. Using the conformal curvature formula, `R_00=3/Omega²` and `R_11=R_22=R_33=1/Omega²`, and since `R=0`, `G_mu nu=R_mu nu`. In particular, `G_11=1/Omega² != 0`. Thus **the trace equation is not equivalent to the full vacuum Einstein equations**.

This is a mathematically explicit failure mode for attempts to derive all of general relativity by varying only a conformal factor. It is compatible with the contracted Bianchi identity: geometric divergence-freeness does not force a tensor to vanish.

The implementation checks this with exact rational polynomial numerators, plus nine regression tests. It does not solve the Einstein equations, claim a physically realized spacetime, or infer quantum/gravitational unification. Full Einstein equations require unconstrained metric variations (with appropriate boundary terms) and an explicit gravitational coupling to matter.

## Reproduce

```sh
python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
python3 -B research/cl_uiot/conformal_trace_counterexample_3p1.py
```

Research-only draft PR #67; no merge, deployment, expenditure, secret use, or self-approval.
