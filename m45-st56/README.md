# M45-ST/56 — Environment-Induced Decoherence

This module implements a minimal **two-qubit unitary interaction** rather than prescribing a dephasing factor directly. The system S starts in `sqrt(p)|0> + sqrt(1-p)|1>`, and the environment E starts in `|0>`. A controlled real rotation maps the joint state to:

`|Psi> = sqrt(p)|00> + sqrt(1-p)|1>(cos(theta)|0> + sin(theta)|1>)`.

The joint system-environment state remains **pure**. Taking the partial trace over E produces:

`rho_S = [[p, sqrt(p(1-p))cos(theta)], [sqrt(p(1-p))cos(theta), 1-p]]`.

The overlap `gamma=cos(theta)` reproduces ST49's reduced phase-damping formula for this initial family. The program computes reduced purity `Tr(rho_S²)`, von Neumann entropy, coherence, and agreement with the phase-damping expression.

```sh
python3 -m unittest discover -s m45-st56 -p 'test_*.py'
python3 m45-st56/environment.py --p 0.5 --theta 1.5707963267948966
```

**Important boundaries:** This is one controlled rotation involving one environment qubit, not an irreversible thermodynamic bath. The joint state is still coherent and can in principle be reversed. Tracing out the environment produces an **improper mixture** and does not select a unique outcome, prove objective collapse, or establish a cosmological ontology. There is no physical hardware or telescope, and no particles are created. CI runs read-only offline tests.
