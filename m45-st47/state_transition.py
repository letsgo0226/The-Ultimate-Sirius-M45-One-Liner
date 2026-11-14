#!/usr/bin/env python3
"""ST47: deterministic one-transition envelope for a GitHub state branch.

This program never calls GitHub. The workflow provides serialized, non-force commits.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("m45_st45",ROOT/"m45-st45"/"unified_machine.py")
machine=importlib.util.module_from_spec(spec)
spec.loader.exec_module(machine)

PROTOCOL="M45-ST47-STATE-v1"

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def digest(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

def seal(body):
    return {**body,"sha256":digest(body)}

def initial():
    return seal({"protocol":PROTOCOL,"revision":0,"machine":machine.initialize()})

def verify(doc):
    if not isinstance(doc,dict) or set(doc)!={"protocol","revision","machine","sha256"}:
        return False
    try:
        if doc["protocol"]!=PROTOCOL or type(doc["revision"]) is not int or doc["revision"]<0:
            return False
        if not machine.verify(doc["machine"]):return False
        return digest({k:v for k,v in doc.items() if k!="sha256"})==doc["sha256"]
    except (TypeError,ValueError,KeyError,OverflowError):
        return False

def advance(doc,expected_revision,action,payload=None):
    if not verify(doc):raise ValueError("invalid state")
    if type(expected_revision) is not int or expected_revision!=doc["revision"]:
        raise ValueError("stale state revision")
    if action=="init":raise ValueError("init is a separate operation")
    updated,receipt=machine.transition(doc["machine"],action,payload)
    # Read-only operations never create new revisions.
    if updated is doc["machine"]:
        return doc,receipt
    next_doc=seal({"protocol":PROTOCOL,"revision":doc["revision"]+1,"machine":updated})
    if not verify(next_doc):raise ValueError("postcondition failed")
    return next_doc,receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input")
    p.add_argument("--output",required=True)
    p.add_argument("--action",required=True,choices=("init",)+machine.TOOLS)
    p.add_argument("--expected-revision",type=int)
    p.add_argument("--payload",default="{}")
    a=p.parse_args()
    payload=json.loads(a.payload)
    if a.action=="init":
        if a.input:raise SystemExit("init must not take existing input")
        result=initial()
        receipt={"initialized":True}
    else:
        if not a.input or a.expected_revision is None:
            raise SystemExit("input and expected revision required")
        path=Path(a.input)
        if path.stat().st_size>2097152:raise SystemExit("state too large")
        doc=json.loads(path.read_text(encoding="utf-8"))
        result,receipt=advance(doc,a.expected_revision,a.action,payload)
    Path(a.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(canonical({"revision":result["revision"],"receipt":receipt,
                     "verified":verify(result),"sha256":result["sha256"]}))
if __name__=="__main__":main()
