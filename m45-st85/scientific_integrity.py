#!/usr/bin/env python3
"""ST85: immutable-policy integrity checks for ST81–ST84 evidence chain.

This is an advisory verifier, not a security sandbox or an approval authority.
No repairs, repository writes, merges, deployments or external calls.
"""
import argparse
import hashlib
import json
from pathlib import Path

PROTOCOLS={
 "audit":"M45-ST81-REPRODUCIBILITY-AUDIT-v1",
 "ledger":"M45-ST82-SCIENTIFIC-EVIDENCE-LEDGER-v1",
 "plan":"M45-ST83-EPISTEMIC-SELF-CORRECTION-v1",
 "governance":"M45-ST84-EPISTEMIC-GOVERNANCE-v1",
}
def fingerprint(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(",",":"),
                                     ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def check_chain(audit,ledger,plan,governance):
    documents={"audit":audit,"ledger":ledger,"plan":plan,"governance":governance}
    violations=[]
    def require(ok,code,detail):
        if not ok:
            violations.append({"code":code,"detail":detail})
    for name,doc in documents.items():
        require(isinstance(doc,dict) and doc.get("protocol")==PROTOCOLS[name],
                "PROTOCOL_MISMATCH",name)
    if violations:
        return report(documents,violations)
    entries=audit.get("stage_results")
    claims=ledger.get("claim_records")
    tasks=plan.get("tasks")
    decisions=governance.get("review_decisions")
    require(isinstance(entries,list),"MALFORMED_AUDIT","stage_results")
    require(isinstance(claims,list),"MALFORMED_LEDGER","claim_records")
    require(isinstance(tasks,list),"MALFORMED_PLAN","tasks")
    require(isinstance(decisions,list),"MALFORMED_GOVERNANCE","review_decisions")
    if not all(isinstance(v,list) for v in (entries,claims,tasks,decisions)):
        return report(documents,violations)
    require(governance.get("source_plan_sha256")==fingerprint(plan),
            "BROKEN_PLAN_BINDING","governance source_plan_sha256")
    require(plan.get("policy")=="ADVISORY_ONLY_NO_EXECUTION_NO_DEPLOYMENT",
            "UNSAFE_PLAN_POLICY","ST83 plan policy")
    require(governance.get("policy")=="READ_ONLY_FAIL_CLOSED_REVIEW_GATE",
            "UNSAFE_GOVERNANCE_POLICY","ST84 policy")
    require(governance.get("execution_enabled") is False,
            "EXECUTION_ENABLED","ST84 execution_enabled")
    require(governance.get("approved_count")==0,
            "APPROVAL_COUNT_NONZERO","ST84 approved_count")
    require(plan.get("scientific_truth_established") is False,
            "UNSUPPORTED_TRUTH_CLAIM","ST83 truth status")
    require(governance.get("pending_count")==len(decisions),
            "PENDING_COUNT_MISMATCH","ST84 count")
    require(plan.get("returned_task_count")==len(tasks),
            "TASK_COUNT_MISMATCH","ST83 count")
    require(ledger.get("claim_count")==len(claims),
            "CLAIM_COUNT_MISMATCH","ST82 count")
    by_stage={}
    for e in entries:
        if not isinstance(e,dict) or not isinstance(e.get("stage"),str) or e["stage"] in by_stage:
            require(False,"INVALID_AUDIT_ENTRY","missing or duplicate stage")
        else:
            by_stage[e["stage"]]=e
    stage_names=set()
    for c in claims:
        if not isinstance(c,dict) or not isinstance(c.get("stage"),str) or c["stage"] in stage_names:
            require(False,"INVALID_CLAIM","missing or duplicate stage")
            continue
        stage=c["stage"]
        stage_names.add(stage)
        status=c.get("execution_evidence_status")
        require(status in ("UNVERIFIED","AUDIT_VERIFIED"),"INVALID_STATUS",stage)
        require(c.get("scientific_truth_status")=="NOT_ESTABLISHED_BY_EXECUTION_AUDIT",
                "UNSUPPORTED_TRUTH_CLAIM",stage)
        checks=c.get("checks")
        if not isinstance(checks,dict):
            require(False,"MISSING_CHECKS",stage)
            continue
        required=("source_present","audit_present","audit_run_passed",
                  "source_hash_matches_audit","output_hash_recorded",
                  "repeatability_confirmed")
        if ledger.get("require_unit_tests") is not False:
            required+=("unit_tests_passed",)
        verified=all(checks.get(k) is True for k in required)
        require((status=="AUDIT_VERIFIED")==verified,
                "EVIDENCE_STATUS_CONTRADICTION",stage)
        audit_entry=by_stage.get(stage)
        if status=="AUDIT_VERIFIED":
            require(isinstance(audit_entry,dict) and audit_entry.get("status")=="pass",
                    "MISSING_PASSING_AUDIT",stage)
            if isinstance(audit_entry,dict):
                require(c.get("current_source_sha256")==audit_entry.get("source_sha256"),
                        "SOURCE_HASH_MISMATCH",stage)
                require(c.get("audit_output_sha256")==audit_entry.get("output_sha256"),
                        "OUTPUT_HASH_MISMATCH",stage)
                require(audit_entry.get("reproducible") is True and
                        audit_entry.get("repeat_output_sha256")==audit_entry.get("output_sha256"),
                        "REPEATABILITY_MISMATCH",stage)
            if ledger.get("require_unit_tests") is not False:
                test=by_stage.get(stage+"-TESTS")
                require(isinstance(test,dict) and test.get("status")=="pass",
                        "MISSING_PASSING_UNIT_TEST",stage)
    require(ledger.get("audit_verified_count")==sum(c.get("execution_evidence_status")=="AUDIT_VERIFIED"
            for c in claims if isinstance(c,dict)),"VERIFIED_COUNT_MISMATCH","ST82 count")
    require(len(decisions)==len(tasks),"DECISION_TASK_COUNT_MISMATCH","ST83/ST84")
    task_hashes={fingerprint(t) for t in tasks if isinstance(t,dict)}
    decision_hashes=set()
    for d in decisions:
        if not isinstance(d,dict):
            require(False,"INVALID_DECISION","nonobject")
            continue
        h=d.get("source_task_sha256")
        require(isinstance(h,str) and h in task_hashes and h not in decision_hashes,
                "BROKEN_TASK_BINDING",str(d.get("stage")))
        if isinstance(h,str):decision_hashes.add(h)
        require(d.get("approved") is False and d.get("execution_permitted") is False
                and d.get("decision")=="PENDING_HUMAN_REVIEW",
                "UNAUTHORIZED_APPROVAL",str(d.get("stage")))
    return report(documents,violations)

def report(documents,violations):
    return {"protocol":"M45-ST85-SCIENTIFIC-INTEGRITY-v1",
            "document_sha256":{k:fingerprint(v) for k,v in documents.items()},
            "passed":not violations,"violation_count":len(violations),
            "violations":violations,"execution_enabled":False,
            "scientific_truth_established":False,
            "policy":"ADVISORY_ONLY_NO_AUTOMATIC_APPROVAL_OR_DEPLOYMENT"}

def main():
    p=argparse.ArgumentParser()
    for name in PROTOCOLS:
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    docs={}
    for name in PROTOCOLS:
        with getattr(a,name).open(encoding="utf-8") as f:
            docs[name]=json.load(f)
    result=check_chain(**docs)
    payload=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if a.output:a.output.write_text(payload,encoding="utf-8")
    print(payload,end="")
    if not result["passed"]:raise SystemExit(1)
if __name__=="__main__":main()
