#!/usr/bin/env python3
"""ST86: bounded, non-approving self-assignment policy."""
import argparse
import json

PROTOCOL = "M45-ST86-CONSTITUTIONAL-SELF-ASSIGNMENT-v1"

def decide(owner, author, is_draft, is_merged=False):
    """Return an auditable assignment proposal; never a review approval."""
    if not all(isinstance(v, str) and v and v.strip() == v for v in (owner, author)):
        raise ValueError("owner and author must be nonempty normalized strings")
    if type(is_draft) is not bool or type(is_merged) is not bool:
        raise ValueError("draft and merged must be booleans")
    eligible = owner == author and not is_draft and not is_merged
    return {
        "protocol": PROTOCOL,
        "eligible": eligible,
        "assignee": owner if eligible else None,
        "reason": ("OWNER_AUTHORED_READY_PR" if eligible
                   else "NOT_OWNER_AUTHORED_OR_NOT_READY"),
        "review_approval_granted": False,
        "merge_permitted": False,
        "execution_permitted": False,
        "independent_review_required": True,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--owner", required=True)
    p.add_argument("--author", required=True)
    p.add_argument("--draft", action="store_true")
    p.add_argument("--merged", action="store_true")
    a = p.parse_args()
    print(json.dumps(decide(a.owner, a.author, a.draft, a.merged),
                     sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
