#!/usr/bin/env python3
"""M45-ST83: fail-closed, advisory-only epistemic self-correction planner.

Reads an ST82 evidence ledger, proposes review tasks and prioritizes them.
Never executes arbitrary suggestions, modifies sources or deploys changes.
"""
import argparse
import json
from pathlib import Path

EXPECTED_PROTOCOL="M45-ST82-SCIENTIFIC-EVIDENCE-LEDGER-v1"
CHECK_TASKS={
    "source_present":("RESTORE_OR_LOCATE_SOURCE",90),
    "audit_present":("RUN_ST81_AUDIT",80),
    "audit_run_passed":("INVESTIGATE_EXECUTION_FAILURE",95),
    "source_hash_matches_audit":("RERUN_AUDIT_FOR_CURRENT_SOURCE",85),
    "output_hash_recorded":("INVESTIGATE_MISSING_OUTPUT_DIGEST",75),
    "repeatability_confirmed":("INVESTIGATE_NONDETERMINISM",95),
    "unit_tests_passed":("REPAIR_OR_RERUN_UNIT_TESTS",90),
}
ORDER=tuple(CHECK_TASKS)

def validate_ledger(data):
    if not isinstance(data,dict) or data.get("protocol")!=EXPECTED_PROTOCOL:
        raise ValueError("expected an ST82 evidence ledger")
    claims=data.get("claim_records")
    if not isinstance(claims,list) or not claims:
        raise ValueError("claim_records must be a nonempty list")
    stages=set()
    for record in claims:
        if not isinstance(record,dict):
            raise ValueError("invalid claim record")
        stage=record.get("stage")
        if not isinstance(stage,str) or not stage or stage in stages:
            raise ValueError("missing or duplicate stage")
        stages.add(stage)
        if record.get("execution_evidence_status") not in ("UNVERIFIED","AUDIT_VERIFIED"):
            raise ValueError("unrecognized evidence status")
        checks=record.get("checks")
        if not isinstance(checks,dict) or any(type(checks.get(k)) is not bool for k in ORDER):
            raise ValueError("missing or malformed evidence checks")
        if record["execution_evidence_status"]=="AUDIT_VERIFIED":
            required=ORDER if data.get("require_unit_tests") is not False else ORDER[:-1]
            if not all(checks[k] for k in required):
                raise ValueError("contradictory verified claim")
    return claims

def plan(data,max_tasks=25):
    if isinstance(max_tasks,bool) or not isinstance(max_tasks,int) or not 1<=max_tasks<=1000:
        raise ValueError("max_tasks must be an integer from 1 to 1000")
    claims=validate_ledger(data)
    tasks=[]
    for record in claims:
        if record["execution_evidence_status"]=="AUDIT_VERIFIED":
            continue
        checks=record["checks"]
        # Only propose a logically useful first repair, not a cascade of
        # downstream tasks whose prerequisites have not been established.
        for key in ORDER:
            if key=="unit_tests_passed" and data.get("require_unit_tests") is False:
                continue
            if not checks[key]:
                action,priority=CHECK_TASKS[key]
                tasks.append({
                    "stage":record["stage"],
                    "action":action,
                    "priority":priority,
                    "failed_check":key,
                    "source_path":record.get("source_path"),
                    "reason":"ST82 evidence check is false; human review required",
                    "requires_human_approval":True,
                    "auto_execute":False
                })
                break
    tasks.sort(key=lambda t:(-t["priority"],t["stage"],t["action"]))
    selected=tasks[:max_tasks]
    return {
        "protocol":"M45-ST83-EPISTEMIC-SELF-CORRECTION-v1",
        "input_claim_count":len(claims),
        "verified_claim_count":sum(r["execution_evidence_status"]=="AUDIT_VERIFIED" for r in claims),
        "unverified_claim_count":sum(r["execution_evidence_status"]=="UNVERIFIED" for r in claims),
        "proposed_task_count":len(tasks),
        "returned_task_count":len(selected),
        "truncated":len(tasks)>len(selected),
        "tasks":selected,
        "policy":"ADVISORY_ONLY_NO_EXECUTION_NO_DEPLOYMENT",
        "scientific_truth_established":False
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--ledger",type=Path,required=True)
    parser.add_argument("--max-tasks",type=int,default=25)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    with args.ledger.open(encoding="utf-8") as f:
        result=plan(json.load(f),args.max_tasks)
    output=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output,encoding="utf-8")
    print(output,end="")
if __name__=="__main__":
    main()
