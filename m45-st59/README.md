# M45-ST/59 — Dynamical Spectrum Broadcasting

This stage bridges the **controlled system–environment unitary interaction** of ST56 and the **spectrum broadcast structure (SBS) criterion** of ST58.

Start with `(sqrt(p)|0> + sqrt(1-p)|1>) ⊗ |0>^N`. Apply N controlled rotations to independent environment qubits. The resulting pure branching state is

`|Psi> = sqrt(p)|0>|0>^N + sqrt(1-p)|1>|e_theta>^N`, with
`|e_theta>=cos(theta)|0>+sin(theta)|1>`.

For an observed fragment of m qubits, tracing out the other N-m yields an off-diagonal block multiplied by `cos(theta)^(N-m)`. The code reports the full two-block trace norm `2 sqrt(p(1-p)) |cos(theta)|^(N-m)`, plus the overlap `|<0|e_theta>|^m` of conditional fragment records.

At `theta=pi/2` (orthogonal conditional records), every **nonempty proper fragment** `1<=m<N` has exactly the SBS form: the unobserved environment removes the off-diagonal block, and each observed record distinguishes pointer values. The full S+E state stays pure and retains cross-branch coherence; **m=N is not an SBS mixture**. For intermediate angles the records are nonorthogonal and this model does not produce exact SBS, even though the cross-block may be small.

```sh
python3 -m unittest discover -s m45-st59 -p 'test_*.py'
python3 m45-st59/dynamical_broadcast.py --n 4 --p 0.5 --theta 1.5707963267948966
```

**Numerical note:** Floating-point cos(pi/2) is approximately 6e-17. The code treats angles within 1e-12 of pi/2 as the ideal orthogonal endpoint for its structural flag; the raw numeric diagnostics remain visible. This is an idealization, not an exact algebraic proof for nearby angles.

**Limitations:** This is a tightly specified pure branching state and analytic reduced-fragment diagnostics, not a generic interacting quantum bath, irreversible dynamics, or a unique-outcome collapse model. It assumes the pointer basis and controlled interactions. No actual particle preparation, observation, or claim that the universe is a computer. Read-only CI.
