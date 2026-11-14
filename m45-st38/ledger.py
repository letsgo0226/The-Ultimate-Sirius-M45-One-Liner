#!/usr/bin/env python3
"""ST38: exact, independently verified SK continuation with an atomic ledger.

The ledger is a single local JSON file atomically replaced after every batch.
No claim of hardware durability or cryptographic authenticity is made.
"""
import argparse
import importlib.util
import json
import os
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m45_st37_exact",HERE.parent/"m45-st37"/"exact.py")
exact=importlib.util.module_from_spec(spec)
spec.loader.exec_module(exact)

PROTOCOL="M45-ST38"
def seal(data):
    result=dict(data)
    result["sha256"]=exact.sha(data)
    return result

def genesis(expression,cap=300):
    exact.parse(expression)
    if type(cap) is not int or not 1<=cap<=300:
        raise ValueError("invalid cap")
    record=seal({"protocol":PROTOCOL,"expression":expression,"cap":cap,"records":[]})
    return record

def verify(ledger):
    if not isinstance(ledger,dict):return False
    try:
        data=dict(ledger)
        claimed=data.pop("sha256")
        if exact.sha(data)!=claimed or data["protocol"]!=PROTOCOL:return False
        original=data["expression"]
        exact.parse(original)
        cap=data["cap"]
        if type(cap) is not int or not 1<=cap<=300:return False
        if not isinstance(data["records"],list):return False
        current=original
        previous="GENESIS"
        terminal=False
        for i,item in enumerate(data["records"]):
            if terminal or not isinstance(item,dict):return False
            if set(item)!={"index","previous","certificate","sha256"}:return False
            content={k:v for k,v in item.items() if k!="sha256"}
            if exact.sha(content)!=item["sha256"]:return False
            if type(item["index"]) is not int or item["index"]!=i:return False
            if item["previous"]!=previous:return False
            cert=item["certificate"]
            if not exact.verify(cert) or cert["expression"]!=current or cert["cap"]!=cap:
                return False
            current=cert["result"]
            previous=item["sha256"]
            terminal=cert["status"]!="PAUSED"
        return True
    except (KeyError,TypeError,ValueError,IndexError,RecursionError,AttributeError):
        return False

def advance(ledger,budget):
    if not verify(ledger):raise ValueError("invalid ledger")
    if type(budget) is not int or not 1<=budget<=100:
        raise ValueError("budget must be 1..100")
    records=ledger["records"]
    if records and records[-1]["certificate"]["status"]!="PAUSED":
        raise ValueError("terminal record: no further continuation")
    current=records[-1]["certificate"]["result"] if records else ledger["expression"]
    cert=exact.certify(current,budget,ledger["cap"])
    if not exact.verify(cert):raise ValueError("independent verification failed")
    item=seal({"index":len(records),"previous":records[-1]["sha256"] if records else "GENESIS",
               "certificate":cert})
    updated=seal({"protocol":PROTOCOL,"expression":ledger["expression"],"cap":ledger["cap"],
                  "records":records+[item]})
    if not verify(updated):raise ValueError("ledger replay failed")
    return updated

def atomic_save(path,ledger):
    if not verify(ledger):raise ValueError("invalid ledger")
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="."+path.name+".",dir=str(path.parent))
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as stream:
            json.dump(ledger,stream,indent=2,ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def load(path):
    ledger=json.loads(Path(path).read_text(encoding="utf-8"))
    if not verify(ledger):raise ValueError("ledger verification failed")
    return ledger

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--file",default="m45-st38-ledger.json")
    p.add_argument("--expression",default="@@@SKKS")
    p.add_argument("--cap",type=int,default=300)
    p.add_argument("--budget",type=int,default=1)
    p.add_argument("--init",action="store_true")
    p.add_argument("--verify-only",action="store_true")
    a=p.parse_args()
    path=Path(a.file)
    if a.init:
        if path.exists():raise SystemExit("Refusing to overwrite existing ledger")
        atomic_save(path,genesis(a.expression,a.cap))
    ledger=load(path)
    if not a.verify_only:
        ledger=advance(ledger,a.budget)
        atomic_save(path,ledger)
    last=ledger["records"][-1]["certificate"] if ledger["records"] else None
    print(json.dumps({"verified":verify(ledger),"batches":len(ledger["records"]),
                      "status":last["status"] if last else "INITIAL",
                      "result":last["result"] if last else ledger["expression"]}))
if __name__=="__main__":main()
