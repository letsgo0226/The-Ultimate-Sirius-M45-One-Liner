# UECV-07: reproducibility manifest
UECV-06 offline CI 44929613686 passed; Lean 44929603954 failed
due to swapped comparison function arguments. Corrected in
5741ae08247c01c6b4c53db08bedcdd7533ec1c2; new CI pending.
UECV-05 test count correction: 1139 arithmetic comparisons.
From a trusted checkout of a specific commit run:
    python3 research/cl_uiot/reproducibility.py > manifest.json
    python3 -B -m unittest discover -s research/cl_uiot -p 'test_*.py' -v
    cd research/cl_uiot
    lake update
    lake exe cache get
    lake build GCAPO
Lean 4.19.0 and Mathlib v4.19.0 are specified; transitive dependencies
and environment are not fully locked. Manifest covers ten selected
files, not the entire dependency closure. It detects changes relative
to a trusted original; it is not signed and does not prove CI success.
Tests check deterministic digest, file mutation and missing files.
No full archival package or independent review yet. No merge/deploy.
