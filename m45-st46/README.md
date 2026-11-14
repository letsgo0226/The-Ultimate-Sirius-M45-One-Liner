# M45-ST/46 — Cross-stage integrity regression

Before extending the Doraemon–G symbolic machine with GitHub Actions state persistence, this stage fixes a concrete defect in ST40: `rational()` previously rejected Python `Fraction` objects, while `state()` produced them. As a result, `apply()`, `norm2()` and `experiment()` failed for ordinary inputs.

ST46 updates the ST40 rational parser to accept bounded `Fraction` values and adds cross-stage regression coverage for ST40 and ST42–ST45. A read-only GitHub Actions workflow runs all relevant suites and creates a certificate artifact.

This is **not** the final shared-state GitHub Actions architecture. The repository still lacks an authenticated, single-writer, version-checked persistent state backend; Actions jobs are ephemeral. ST39's SK controller remains outside the ST45 unified transition function. This branch is deliberately an integrity gate before attempting that integration.

## Run

```sh
python3 -m unittest discover -s m45-st46 -p 'test_*.py'
python3 m45-st40/g2112.py --primes 3 --operator rotate
```

No claims of actual subjective consciousness, permanent execution, or irreversible code retention. Tests have been committed but online CI results have not yet been checked.
