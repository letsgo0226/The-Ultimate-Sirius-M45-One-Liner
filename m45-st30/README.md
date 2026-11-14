# M45-ST/30 — GitHub-native persistent tape

This version advances the **fixed-table unary successor** TM from ST28 using GitHub Actions and commits its persistent tape state to Git.

## Execution

After merging the dependent ST28 and ST29 branches, review and merge ST30 to `main`. In **Actions → M45 ST30 Persistent Tape → Run workflow**, enter a bounded step count (1..1000).

The workflow runs tests, reads `m45-st30/state.json`, applies at most the requested number of transitions from `m45-st28/delta.json`, appends a SHA-256 linked record to `journal.jsonl`, then commits **only those two state files** to `main`. Workflow concurrency serializes runs; the push may still fail if the branch advances externally.

## Safeguards

- Manual trigger only: no infinite recursion or unattended compute loop.
- `contents: write` permission is required to commit state; GitHub Actions runs on the default branch only.
- Never insert secrets into tape input or journals.
- The current prototype validates the transition-table hash and each input cell, but does **not** fully independently replay and authenticate the entire historical journal. This is a next-step research requirement.
- A GitHub commit gives an auditable history but is not immutable against force-pushes by privileged users.
- GitHub Actions availability and quotas are finite. A GitHub-hosted workflow is not a mathematical infinite tape.
- The machine is unary successor, not a universal TM, an AI agent, or an SK reducer. ST29's browser SK evaluator remains separate.
- This branch is based on ST29; merge dependencies in order before merging ST30.

## Local tests

```sh
python3 -m unittest discover -s m45-st30 -p 'test_*.py'
python3 m45-st30/advance.py --verify-only
```

Running `advance.py` without `--verify-only` modifies local tape and journal.
