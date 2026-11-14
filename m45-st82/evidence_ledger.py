#!/usr/bin/env python3
"""ST82: conservative evidence ledger for the M45 toy-model research chain.

A source file or a declared theorem is not execution evidence. The ledger
binds stage claims to an ST81 audit report and checks source hashes against
the current checkout. Without audit evidence, status remains UNVERIFIED.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
STAGES={
 "ST64":("m45-st64/frame_switch.py","Finite Z2 relational frame-switch invariance",
         "Four-amplitude invariant-sector toy model; not general quantum reference frames"),
 "ST68":("m45-st68/quantum_metrology.py","Finite-model QFI/frame covariance",
         "Pure-state parameter encoding; not a hardware metrology demonstration"),
 "ST69":("m45-st69/observer_estimation.py","Paired observer Born-probability agreement",
         "Ideal independent Bernoulli simulation under one chosen state family"),
 "ST73":("m45-st73/adaptive_design.py","Adaptive allocation and conservative confidence intervals",
         "Independent stationary symmetric detector flips; specified sampling assumptions"),
 "ST74":("m45-st74/active_learning_benchmark.py","Paired active-learning benchmark",
         "Finite Monte Carlo sample; no universal policy superiority"),
 "ST75":("m45-st75/information_gain.py","Approximate expected-risk allocation",
         "Delta-method posterior risk surrogate, not exact mutual information"),
 "ST76":("m45-st76/bayesian_model_selection.py","Discrete-grid Bayesian model comparison",
         "Prior/grid dependent; model probabilities do not prove truth"),
 "ST77":("m45-st77/predictive_criticism.py","Held-out posterior predictive criticism",
         "Tail areas are descriptive, not calibrated frequentist p-values"),
 "ST78":("m45-st78/model_expansion.py","Bounded candidate expansion with locked testing",
         "Predeclared families, not open-ended discovery"),
 "ST79":("m45-st79/model_evolution.py","Auditable bounded candidate mutations",
         "Heuristic penalty and one locked evaluation"),
 "ST80":("m45-st80/discovery_benchmark.py","Paired out-of-sample model benchmark",
         "Simulated data and descriptive Monte Carlo summaries"),
}
NOT_ESTABLISHED=(
 "Quantum hardware validation",
 "A new physical law",
 "Autonomous open-ended scientific discovery",
 "General quantum reference-frame equivalence",
 "A metaphysical theorem or universal oracle",
)

def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_audit(path):
    if path is None:
        return None
    with open(path,encoding="utf-8") as f:
        data=json.load(f)
    if not isinstance(data,dict) or data.get("protocol")!="M45-ST81-REPRODUCIBILITY-AUDIT-v1":
        raise ValueError("not an ST81 audit report")
    entries=data.get("stage_results")
    if not isinstance(entries,list):
        raise ValueError("missing stage_results")
    seen=set()
    for e in entries:
        if not isinstance(e,dict) or not isinstance(e.get("stage"),str):
            raise ValueError("invalid audit entry")
        if e["stage"] in seen:
            raise ValueError("duplicate audit stage")
        seen.add(e["stage"])
    return {e["stage"]:e for e in entries}

def ledger(audit_path=None,require_tests=True):
    entries=load_audit(audit_path)
    claims=[]
    for stage,(rel,claim,scope) in STAGES.items():
        path=ROOT/rel
        source_hash=sha256_file(path) if path.is_file() else None
        run=entries.get(stage) if entries is not None else None
        test=entries.get(stage+"-TESTS") if entries is not None else None
        checks={
            "source_present":source_hash is not None,
            "audit_present":run is not None,
            "audit_run_passed":bool(run and run.get("status")=="pass"),
            "source_hash_matches_audit":bool(run and source_hash is not None
                                               and run.get("source_sha256")==source_hash),
            "output_hash_recorded":bool(run and isinstance(run.get("output_sha256"),str)
                                        and len(run["output_sha256"])==64
                                        and all(c in "0123456789abcdef" for c in run["output_sha256"])),
            "repeatability_confirmed":bool(run and run.get("reproducible") is True
                                           and run.get("repeat_output_sha256")==run.get("output_sha256")),
            "unit_tests_passed":bool(test and test.get("status")=="pass")
        }
        needed=("source_present","audit_present","audit_run_passed",
                "source_hash_matches_audit","output_hash_recorded","repeatability_confirmed")
        if require_tests:
            needed+=("unit_tests_passed",)
        verified=all(checks[k] for k in needed)
        claims.append({
            "stage":stage,"claim":claim,"scope_and_limitations":scope,
            "source_path":rel,"current_source_sha256":source_hash,
            "audit_output_sha256":run.get("output_sha256") if run else None,
            "checks":checks,
            "execution_evidence_status":"AUDIT_VERIFIED" if verified else "UNVERIFIED",
            "scientific_truth_status":"NOT_ESTABLISHED_BY_EXECUTION_AUDIT"
        })
    return {
        "protocol":"M45-ST82-SCIENTIFIC-EVIDENCE-LEDGER-v1",
        "audit_supplied":audit_path is not None,
        "require_unit_tests":require_tests,
        "claim_records":claims,
        "audit_verified_count":sum(x["execution_evidence_status"]=="AUDIT_VERIFIED" for x in claims),
        "claim_count":len(claims),
        "not_established_claims":list(NOT_ESTABLISHED),
        "interpretation":"AUDIT_VERIFIED_MEANS_REPRODUCIBLE_EXECUTION_ONLY_NOT_PHYSICAL_OR_MATHEMATICAL_PROOF"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audit",type=Path,help="ST81 JSON audit file; omitted means no execution evidence")
    ap.add_argument("--allow-missing-tests",action="store_true",
                    help="Require run/hash/repeatability but not unittest evidence")
    ap.add_argument("--output",type=Path,help="Optional JSON output path")
    ap.add_argument("--require-verified",action="store_true",
                    help="Exit nonzero unless all stage claims have matching audit evidence")
    args=ap.parse_args()
    result=ledger(args.audit,not args.allow_missing_tests)
    output=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.output:
        args.output.write_text(output,encoding="utf-8")
    print(output,end="")
    if args.require_verified and result["audit_verified_count"]!=result["claim_count"]:
        raise SystemExit(1)
if __name__=="__main__":main()
