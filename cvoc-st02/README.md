# CVOC-ST02 — Read-only staging adapter

This is a manifest-and-bytes contract validator, **not** a native ST30–ST47 verifier and **not** an executable continuous compute service.

Run: `python3 -m unittest discover -s cvoc-st02 -p 'test_*.py' -v`.

GitHub Actions is read-only, triggered by PR changes or manual dispatch, with no schedule, write token, persistent state updates, deployment, secrets, or arbitrary code execution API. The 40-hex source_commit is only syntax-checked; Git provenance is not authenticated. The 12 unit tests check this adapter alone.

Do not merge or enable automated scheduling without independent review.
