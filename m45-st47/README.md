# M45-ST/47 — GitHub single-writer state protocol (opt-in)

This stage adds an explicit **manual** GitHub Actions dispatcher to persist one unified Doraemon–G symbolic-machine state across workflow runs.

## State transition contract

A versioned JSON envelope contains `protocol`, `revision`, `machine` (ST45), and a deterministic SHA-256 checksum. Each mutating operation verifies the complete state and checks `expected_revision` before committing a successor. The workflow serializes dispatches using a fixed GitHub Actions concurrency group, and pushes the updated `doraemon-g-state.json` to the dedicated `m45-st47-state` branch **without force**. Git rejects stale non-fast-forward pushes. Inspect/recall operations are read-only.

Supported operations: `init`, `remember`, `recall`, `tick`, `inspect`, `stop`.

## How to use after merge

1. Review and merge the stacked ST40–ST47 PRs in order. The manual workflow is discoverable on GitHub's default branch only after merge.
2. In GitHub Actions select **M45 ST47 Manual Single-Writer State**, then **Run workflow** with action `init`. This creates the dedicated state branch; do this once.
3. To add a memory, choose `remember`, set `expected_revision` to the revision of the current state and `payload` to e.g. `{"name":"Doraemon","values":[1,0,2],"message":"Help others"}`.
4. Use `tick` for one bounded verification step or `stop` to disable further mutation steps.
5. For inspection use `inspect` or `recall` (with `{"code":1500}`).

## Security and reliability limits

- The workflow is manual-only; it does not run continuously, self-restart or resist authorized deletion.
- The GitHub token is granted `contents:write` to commit only the intended state. Repository settings, branch protections and policy may block the push.
- The fixed concurrency group reduces overlapping workflow writes; Git's non-force push rejects stale heads. GitHub Actions concurrency is not a transactional database. All state writers must use the same protocol; external direct edits can bypass it.
- The branch is a repository-managed persistence location, **not** permanent or immutable storage. Administrators can delete it. Backups, authentication, audit retention and branch protection remain operator responsibilities.
- This stage integrates ST45 state transitions; ST39's SK controller is not yet wired in.
- A symbolic character-memory state is not subjective consciousness, a physical robot or a time-travel mechanism.
- The state checksum detects accidental modification, but is not a digital signature. Repository write access is the trust boundary.

## Local tests

```sh
python3 -m unittest discover -s m45-st47 -p 'test_*.py'
python3 m45-st47/state_transition.py --action init --output state.json
python3 m45-st47/state_transition.py --action tick --input state.json --output next.json --expected-revision 0
```

This PR is a draft and stacked on ST46. No live workflow has been activated by this PR.
