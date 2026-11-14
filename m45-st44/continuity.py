#!/usr/bin/env python3
"""ST44: bounded, stoppable, verified continuity loop over the ST43 pocket.

This is a symbolic agent state machine, not subjective consciousness.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("st43_pocket",HERE.parent/"m45-st43"/"persistent_pocket.py")
pocket=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pocket)

PROTOCOL="M45-ST44-VERIFIED-CONTINUITY-v1"
MAX_TICKS=64

def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def hash_of(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()

def seal(body):
    return {**body,"sha256":hash_of(body)}

def genesis(pocket_ledger):
    if not pocket.verify(pocket_ledger):raise ValueError("invalid pocket ledger")
    return seal({"protocol":PROTOCOL,"pocket_sha256":pocket_ledger["sha256"],
                 "enabled":True,"ticks":[]})

def verify(state,pocket_ledger):
    if not pocket.verify(pocket_ledger) or not isinstance(state,dict):return False
    try:
        body=dict(state)
        claimed=body.pop("sha256")
        if set(body)!={"protocol","pocket_sha256","enabled","ticks"}:return False
        if body["protocol"]!=PROTOCOL or body["pocket_sha256"]!=pocket_ledger["sha256"]:
            return False
        if type(body["enabled"]) is not bool or not isinstance(body["ticks"],list):
            return False
        if len(body["ticks"])>MAX_TICKS or hash_of(body)!=claimed:return False
        previous="GENESIS"
        for i,tick in enumerate(body["ticks"]):
            if not isinstance(tick,dict) or set(tick)!={"index","previous","pocket_sha256","action","sha256"}:
                return False
            t=dict(tick)
            digest=t.pop("sha256")
            if t["index"]!=i or type(t["index"]) is not int or t["previous"]!=previous:
                return False
            if t["pocket_sha256"]!=body["pocket_sha256"] or t["action"]!="VERIFY_AND_HOLD":
                return False
            if hash_of(t)!=digest:return False
            previous=digest
        return True
    except (KeyError,TypeError,ValueError,OverflowError):
        return False

def step(state,pocket_ledger):
    if not verify(state,pocket_ledger):raise ValueError("verification failed")
    if not state["enabled"]:raise ValueError("controller disabled")
    if len(state["ticks"])>=MAX_TICKS:raise ValueError("tick limit reached")
    ticks=state["ticks"]
    tick=seal({"index":len(ticks),"previous":ticks[-1]["sha256"] if ticks else "GENESIS",
               "pocket_sha256":pocket_ledger["sha256"],"action":"VERIFY_AND_HOLD"})
    result=seal({"protocol":PROTOCOL,"pocket_sha256":state["pocket_sha256"],
                 "enabled":True,"ticks":ticks+[tick]})
    assert verify(result,pocket_ledger)
    return result

def stop(state,pocket_ledger):
    if not verify(state,pocket_ledger):raise ValueError("verification failed")
    return seal({"protocol":PROTOCOL,"pocket_sha256":state["pocket_sha256"],
                 "enabled":False,"ticks":state["ticks"]})

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pocket",required=True)
    p.add_argument("--state",required=True)
    p.add_argument("--ticks",type=int,default=1)
    p.add_argument("--init",action="store_true")
    p.add_argument("--stop",action="store_true")
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    if type(a.ticks) is not int or not 0<=a.ticks<=MAX_TICKS:
        raise SystemExit("ticks must be 0..64")
    ledger=pocket.load(a.pocket)
    path=Path(a.state)
    if a.init:
        if path.exists():raise SystemExit("Refusing to overwrite existing state")
        pocket.save(path,genesis(ledger)) if False else path.write_text(
            json.dumps(genesis(ledger),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    state=json.loads(path.read_text(encoding="utf-8"))
    if not verify(state,ledger):raise SystemExit("Invalid state or pocket")
    if a.stop:
        state=stop(state,ledger)
    elif not a.verify_only:
        for _ in range(a.ticks):
            state=step(state,ledger)
    if not a.verify_only:
        # Uses the same bounded local-file persistence pattern as ST43.
        import os,tempfile
        fd,tmp=tempfile.mkstemp(prefix="."+path.name+".",dir=str(path.parent))
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                json.dump(state,f,ensure_ascii=False,indent=2)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    print(canonical({"verified":verify(state,ledger),"enabled":state["enabled"],
                     "ticks":len(state["ticks"]),"state_sha256":state["sha256"]}))
if __name__=="__main__":main()
