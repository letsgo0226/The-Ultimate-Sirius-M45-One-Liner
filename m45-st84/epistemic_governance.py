#!/usr/bin/env python3
"""ST84: read-only, fail-closed governance of ST83 epistemic repair proposals.

No commands, file edits, deployments, approvals, or network requests occur.
"""
import argparse
import hashlib
import json
from pathlib import Path

PROTOCOL="M45-ST83-EPISTEMIC-SELF-CORRECTION-v1"
POLICY={
 "INVESTIGATE_NONDETERMINISM":("high","independent_reviewer"),
 "INVESTIGATE_EXECUTION_FAILURE":("high","independent_reviewer"),
 "RESTORE_OR_LOCATE_SOURCE":("high","independent_reviewer"),
 "REPAIR_OR_RERUN_UNIT_TESTS":("high","independent_reviewer"),
 "RERUN_AUDIT_FOR_CURRENT_SOURCE":("medium","maintainer"),
 "RUN_ST81_AUDIT":("low","maintainer"),
 "INVESTIGATE_MISSING_OUTPUT_DIGEST":("medium","maintainer"),
}
CHECK_TO_ACTION={
 "source_present":"RESTORE_OR_LOCATE_SOURCE",
 "audit_present":"RUN_ST81_AUDIT",
 "audit_run_passed":"INVESTIGATE_EXECUTION_FAILURE",
 "source_hash_matches_audit":"RERUN_AUDIT_FOR_CURRENT_SOURCE",
 "output_hash_recorded":"INVESTIGATE_MISSING_OUTPUT_DIGEST",
 "repeatability_confirmed":"INVESTIGATE_NONDETERMINISM",
 "unit_tests_passed":"REPAIR_OR_RERUN_UNIT_TESTS",
}
RANK={"low":1,"medium":2,"high":3}
def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),
                                     ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def govern(plan):
    if not isinstance(plan,dict) or plan.get("protocol")!=PROTOCOL:
        raise ValueError("expected an ST83 correction plan")
    tasks=plan.get("tasks")
    if not isinstance(tasks,list) or len(tasks)>1000:
        raise ValueError("invalid task list")
    if plan.get("returned_task_count")!=len(tasks):
        raise ValueError("task count mismatch")
    if plan.get("policy")!="ADVISORY_ONLY_NO_EXECUTION_NO_DEPLOYMENT":
        raise ValueError("untrusted plan policy")
    if plan.get("scientific_truth_established") is not False:
        raise ValueError("unexpected scientific truth claim")
    decisions=[]
    seen=set()
    for task in tasks:
        if not isinstance(task,dict):
            raise ValueError("invalid task")
        action=task.get("action")
        stage=task.get("stage")
        failed=task.get("failed_check")
        if action not in POLICY or CHECK_TO_ACTION.get(failed)!=action:
            raise ValueError("unknown or inconsistent action")
        if not isinstance(stage,str) or not stage or (stage,action) in seen:
            raise ValueError("missing or duplicate task identity")
        seen.add((stage,action))
        if task.get("requires_human_approval") is not True or task.get("auto_execute") is not False:
            raise ValueError("ST83 task must be advisory-only")
        priority=task.get("priority")
        if type(priority) is not int or not 0<=priority<=100:
            raise ValueError("invalid priority")
        risk,reviewer=POLICY[action]
        # Approval is NEVER inferred from a task or the input document.
        decisions.append({
            "stage":stage,"action":action,"failed_check":failed,
            "risk":risk,"required_reviewer_role":reviewer,
            "source_task_sha256":canonical_hash(task),
            "decision":"PENDING_HUMAN_REVIEW",
            "approved":False,
            "execution_permitted":False,
            "rollback_required_if_implemented":RANK[risk]>=2,
            "required_evidence":[
                "independent_review_record",
                "fresh_stage_unit_tests",
                "fresh_ST81_ST82_audit",
                "separate_implementation_pull_request"
            ]
        })
    decisions.sort(key=lambda d:(-RANK[d["risk"]],d["stage"],d["action"]))
    return {
        "protocol":"M45-ST84-EPISTEMIC-GOVERNANCE-v1",
        "source_plan_sha256":canonical_hash(plan),
        "review_decisions":decisions,
        "pending_count":len(decisions),
        "approved_count":0,
        "execution_enabled":False,
        "policy":"READ_ONLY_FAIL_CLOSED_REVIEW_GATE",
        "note":"Risk levels are predefined policy heuristics, not empirical safety guarantees"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--plan",required=True,type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    with args.plan.open(encoding="utf-8") as f:
        result=govern(json.load(f))
    payload=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    print(payload,end="")
if __name__=="__main__":main()
