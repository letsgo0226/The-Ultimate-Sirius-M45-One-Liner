# M45-ST/86 — Constitutional Self-Assignment

This is a **bounded task ownership** feature, not autonomous review approval.

On an owner-authored, non-draft, unmerged pull request, the GitHub Actions
`pull_request_target` workflow assigns the repository owner as the PR assignee.
It uses event metadata only and **never checks out or runs PR-supplied code**
with write credentials. Other PRs are not assigned by this policy.

The pure Python policy in `self_assignment.py` is independently unit-testable.
Use `python3 -m unittest discover -s m45-st86 -p 'test_*.py'`.

**Governance constraints:** Assignee != Reviewer. Assignment does not grant
review approval, permit merging, establish scientific truth, or run deployments.
Independent human review and repository branch protection remain separate.

This first version does **not** autonomously create issues, dispatch coding
agents, or schedule recurring monitoring. Workflow triggers only on the
specified PR events. GitHub Actions permissions and repository settings may
prevent assignment; failures must be inspected rather than assumed successful.
