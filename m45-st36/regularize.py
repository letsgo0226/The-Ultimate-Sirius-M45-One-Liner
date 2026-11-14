#!/usr/bin/env python3
"""ST36: testable regularization of finite SK computation by bounded resource budgets.

This does not compute a mathematical singularity or evade undecidability.
"""
import argparse
import hashlib
import json
from pathlib import Path
import importlib.util

BASE=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("st32_sk",BASE/"m45-st32"/"sk_tape.py")
SK=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SK)

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def sha(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()

def evaluate(expr,budget=8,tape_cap=10000):
    if type(budget) is not int or not 0<=budget<=1000:
        raise ValueError("budget must be 0..1000")
    if type(tape_cap) is not int or not 1<=tape_cap<=10000:
        raise ValueError("tape cap must be 1..10000")
    tree=SK.parse(expr)
    current=SK.encode(tree)
    if len(current)>tape_cap:
        return {"input":expr,"result":current,"status":"CAP_EXCEEDED","steps":0,
                "budget":budget,"tape_cap":tape_cap,"trace":[]}
    trace=[]
    status="PAUSED"
    for _ in range(budget):
        nxt=SK.reduce_once(tree)
        if nxt is None:
            status="NORMAL"
            break
        new=SK.encode(nxt)
        if len(new)>tape_cap:
            status="CAP_EXCEEDED"
            break
        trace.append({"before":current,"after":new,"length":len(new)})
        tree=nxt
        current=new
    else:
        if SK.reduce_once(tree) is None:
            status="NORMAL"
    return {"input":expr,"result":current,"status":status,"steps":len(trace),
            "budget":budget,"tape_cap":tape_cap,"trace":trace}

def experiment(expr,budgets=(0,1,2,4,8,16,32),tape_cap=10000):
    if not budgets or any(type(b) is not int or not 0<=b<=1000 for b in budgets):
        raise ValueError("invalid budget schedule")
    runs=[evaluate(expr,b,tape_cap) for b in budgets]
    # The observable is only stabilization under tested finite budgets.
    normal=next((r for r in runs if r["status"]=="NORMAL"),None)
    report={"protocol":"M45-ST36","hypothesis":"finite-resource regularization",
            "expression":expr,"runs":runs,
            "observed_normal_form":normal["result"] if normal else None,
            "conclusion":"NORMAL_OBSERVED" if normal else "UNRESOLVED_WITHIN_TESTED_BUDGETS"}
    report["sha256"]=sha(report)
    return report

def verify(report):
    signed=dict(report)
    claimed=signed.pop("sha256",None)
    if claimed!=sha(signed):return False
    try:
        expected=experiment(signed["expression"],tuple(r["budget"] for r in signed["runs"]),
                            signed["runs"][0]["tape_cap"])
        return expected==report
    except (ValueError,KeyError,TypeError,IndexError):
        return False

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--expression",default="@@@SKKS")
    p.add_argument("--tape-cap",type=int,default=10000)
    p.add_argument("--out",default="m45-st36-regularization.json")
    a=p.parse_args()
    result=experiment(a.expression,tape_cap=a.tape_cap)
    assert verify(result)
    Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(canonical({"conclusion":result["conclusion"],
                     "observed_normal_form":result["observed_normal_form"],
                     "sha256":result["sha256"]}))
