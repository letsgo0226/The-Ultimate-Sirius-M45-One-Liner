#!/usr/bin/env python3
"""ST39: finite, fail-closed controller for exact persistent SK computation."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m45_st38_ledger",HERE.parent/"m45-st38"/"ledger.py")
ledger_mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger_mod)

def policy(max_batches=8,steps_per_batch=1,max_total_steps=32):
    values=(max_batches,steps_per_batch,max_total_steps)
    if any(type(v) is not int for v in values):
        raise ValueError("policy values must be integers")
    if not (1<=max_batches<=100 and 1<=steps_per_batch<=100 and 1<=max_total_steps<=10000):
        raise ValueError("policy values out of range")
    return {"max_batches":max_batches,"steps_per_batch":steps_per_batch,
            "max_total_steps":max_total_steps}

def inspect(state,limits):
    """Pure deterministic decision. Does not mutate persistent state."""
    if not ledger_mod.verify(state):
        return {"action":"BLOCK","reason":"INVALID_LEDGER"}
    limits=policy(**limits)
    records=state["records"]
    used=sum(r["certificate"]["steps"] for r in records)
    if records:
        status=records[-1]["certificate"]["status"]
        if status!="PAUSED":
            return {"action":"STOP","reason":status}
    if len(records)>=limits["max_batches"]:
        return {"action":"STOP","reason":"BATCH_LIMIT"}
    remaining=limits["max_total_steps"]-used
    if remaining<=0:
        return {"action":"STOP","reason":"STEP_LIMIT"}
    return {"action":"ADVANCE","budget":min(limits["steps_per_batch"],remaining),
            "reason":"VERIFIED_AND_WITHIN_LIMITS"}

def run(state,limits):
    """Run a finite number of batches; verify before and after every batch."""
    limits=policy(**limits)
    if not ledger_mod.verify(state):
        raise ValueError("invalid initial ledger")
    decisions=[]
    while True:
        decision=inspect(state,limits)
        decisions.append(decision)
        if decision["action"]!="ADVANCE":
            break
        updated=ledger_mod.advance(state,decision["budget"])
        if not ledger_mod.verify(updated):
            raise ValueError("post-advance verification failed")
        state=updated
    return state,decisions

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--file",default="m45-st39-ledger.json")
    p.add_argument("--expression",default="@@@SKKS")
    p.add_argument("--cap",type=int,default=300)
    p.add_argument("--max-batches",type=int,default=8)
    p.add_argument("--steps-per-batch",type=int,default=1)
    p.add_argument("--max-total-steps",type=int,default=32)
    p.add_argument("--init",action="store_true")
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    limits=policy(a.max_batches,a.steps_per_batch,a.max_total_steps)
    path=Path(a.file)
    if a.init:
        if path.exists():raise SystemExit("Refusing to overwrite existing ledger")
        ledger_mod.atomic_save(path,ledger_mod.genesis(a.expression,a.cap))
    state=ledger_mod.load(path)
    if a.verify_only:
        decisions=[inspect(state,limits)]
    else:
        # Persist after EACH batch, not only after the controller loop.
        decisions=[]
        while True:
            decision=inspect(state,limits)
            decisions.append(decision)
            if decision["action"]!="ADVANCE":break
            state=ledger_mod.advance(state,decision["budget"])
            ledger_mod.atomic_save(path,state)
            state=ledger_mod.load(path)
    print(json.dumps({"verified":ledger_mod.verify(state),"batches":len(state["records"]),
                      "decision":decisions[-1],"total_steps":sum(
                      r["certificate"]["steps"] for r in state["records"])}))

if __name__=="__main__":
    main()
