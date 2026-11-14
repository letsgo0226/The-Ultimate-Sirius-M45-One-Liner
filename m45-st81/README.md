# M45-ST/81 — Relational Quantum Reproducibility and Scientific Audit

This stage adds a **cross-stage, deterministic execution and unit-test audit** for M45-ST64, ST68, ST69, and ST73–ST80. It is intentionally a verification stage rather than another theoretical extension.

## What is audited

- Each stage is invoked as an independent Python subprocess with bounded, fixed arguments.
- Each stage must exit successfully and produce a JSON object with a nonempty `protocol` field.
- Canonically serialized JSON outputs are hashed with SHA-256 and rerun with the same arguments; the hashes must match.
- Source files are hashed so that results can be associated with exact content.
- Optional `--run-tests` runs each stage's own unittest discovery and records pass/fail plus error excerpts.
- All results are combined in one JSON audit report; the command exits nonzero if any stage fails.
- GitHub Actions runs the audit with read-only repository permissions and uploads the JSON as a build artifact.

```sh
python3 -m unittest discover -s m45-st81 -p 'test_*.py'
python3 m45-st81/reproducibility_audit.py --run-tests --output m45-st81-audit.json
```

## Scope and limitations

This is **not** a proof of physical correctness, theoretical consistency, model calibration, or reproducibility across different Python versions/platforms. SHA-256 output equality demonstrates repeatability only for the tested commands and runtime environment. Tests may miss defects, and passing one random seed does not establish statistical validity. The cross-stage audit does not merge or modify upstream pull requests, and stacked branches should be merged in dependency order. Review failures before interpreting downstream benchmark results. CI and independent execution remain pending until workflow results are inspected.

## Integration correction

The ST79 mutation-locality unit test is corrected in this branch to avoid a false failure caused by probability clipping at the upper boundary. This test-only fix belongs to the ST81 stacked branch and must be backported or merged in order; it does not automatically modify the earlier ST79 draft PR.
