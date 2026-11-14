#!/usr/bin/env python3
"""ST43: persistent, verified fictional pocket records with finite resource policy."""
import argparse
import importlib.util
import json
import os
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("m45_st42_pocket",HERE.parent/"m45-st42"/"pocket.py")
pocket=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pocket)

PROTOCOL="M45-ST43-POCKET-LEDGER-v1"
MAX_RECORDS=64
MAX_BYTES=1048576

def seal(data):
    return {**data,"sha256":pocket.digest(data)}

def genesis():
    return seal({"protocol":PROTOCOL,"events":[]})

def verify(ledger):
    if not isinstance(ledger,dict):return False
    try:
        body=dict(ledger)
        claimed=body.pop("sha256")
        if set(body)!={"protocol","events"} or body["protocol"]!=PROTOCOL:
            return False
        if pocket.digest(body)!=claimed:return False
        events=body["events"]
        if not isinstance(events,list) or len(events)>MAX_RECORDS:return False
        previous="GENESIS"
        for index,event in enumerate(events):
            if not isinstance(event,dict) or set(event)!={"index","previous","record","sha256"}:
                return False
            if type(event["index"]) is not int or event["index"]!=index:return False
            if event["previous"]!=previous:return False
            if not pocket.verify(event["record"]):return False
            item=dict(event)
            sha=item.pop("sha256")
            if pocket.digest(item)!=sha:return False
            previous=sha
        return len(pocket.canonical(ledger).encode("utf-8"))<=MAX_BYTES
    except (ValueError,TypeError,KeyError,OverflowError):
        return False

def append(ledger,record):
    if not verify(ledger):raise ValueError("invalid ledger")
    if not pocket.verify(record):raise ValueError("invalid record")
    events=ledger["events"]
    if len(events)>=MAX_RECORDS:raise ValueError("record limit reached")
    event=seal({"index":len(events),"previous":events[-1]["sha256"] if events else "GENESIS",
                "record":record})
    result=seal({"protocol":PROTOCOL,"events":events+[event]})
    if not verify(result):raise ValueError("new ledger invalid or size limit exceeded")
    return result

def lookup(ledger,code):
    if not verify(ledger):raise ValueError("invalid ledger")
    return pocket.retrieve([e["record"] for e in ledger["events"]],code)

def save(path,ledger):
    if not verify(ledger):raise ValueError("invalid ledger")
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix="."+path.name+".",dir=str(path.parent))
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(ledger,f,ensure_ascii=False,indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def load(path):
    path=Path(path)
    if path.stat().st_size>MAX_BYTES*2:
        raise ValueError("file exceeds maximum read size")
    data=json.loads(path.read_text(encoding="utf-8"))
    if not verify(data):raise ValueError("ledger verification failed")
    return data

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--file",default="m45-st43-ledger.json")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("init")
    add=sub.add_parser("add")
    add.add_argument("--name",required=True)
    add.add_argument("--values",required=True)
    add.add_argument("--message",required=True)
    get=sub.add_parser("get")
    get.add_argument("--code",required=True,type=int)
    sub.add_parser("verify")
    args=p.parse_args()
    path=Path(args.file)
    if args.command=="init":
        if path.exists():raise SystemExit("Refusing to overwrite existing ledger")
        save(path,genesis())
        print("initialized")
        return
    ledger=load(path)
    if args.command=="add":
        values=[int(v) for v in args.values.split(",")]
        record=pocket.pocket_record(args.name,values,args.message)
        save(path,append(ledger,record))
        print(json.dumps({"stored":True,"godel_number":record["godel_number"]}))
    elif args.command=="get":
        print(json.dumps(lookup(ledger,args.code),ensure_ascii=False,indent=2))
    else:
        print(json.dumps({"verified":True,"records":len(ledger["events"])}))

if __name__=="__main__":main()
