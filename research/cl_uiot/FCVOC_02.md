# FCVOC-02: finite machine
Three control states (0,1,halt), four head positions and four binary cells
yield 192 configurations. The fixed transition reads and flips a cell,
updates the control and moves the head; halt is absorbing. Reflection
negates head position and tape index and reverses movement handedness.
For all valid states, J T+ = T- J, by index substitution; induction
extends the identity to any finite number of steps. Tests enumerate all
192 states and selected iteration budgets. The spectral transition is
defined by decode-step-encode, not an independent frequency-native
implementation or independent verifier. Runtime is capped at 1024 steps.
Pure functions; no network, subprocess, replication or permissions.
Finite model, not universal computation or persistent execution.
Lean formalization and independent spectral update remain future work.
