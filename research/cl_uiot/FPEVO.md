# FPEVO — reproducible Lean environment draft
From research/cl_uiot, with trusted elan installed:
```sh
lake update
lake exe cache get
lake build GCAPO
```
Lean and Mathlib release versions are selected as v4.19.0. The transitive lake-manifest.json must still be generated and reviewed. These commands require network access and local disk resources. No new CI workflow is enabled, no paid runner or deployment is authorized, and no command has been executed in a Lean environment in this milestone. Existing Python CI is not a Lean validation. Review the dependency manifest and actual compiler output before declaring success.
