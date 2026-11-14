#!/usr/bin/env python3
"""ST45: bounded Doraemon-inspired symbolic machine; no consciousness claim."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

st42=module("m45_st42",Path("m45-st42/pocket.py"))
st43=module("m45_st43",Path("m45-st43/persistent_pocket.py"))
st44=module("m45_st44",Path("m45-st44/continuity.py"))

PROTOCOL="M45-ST45-UNIFIED-MACHINE-v1"
TOOLS=("remember","recall","tick","stop","inspect")

def initialize():
    pocket=st43.genesis()
    return {"protocol":PROTOCOL,"pocket":pocket,"controller":st44.genesis(pocket)}

def verify(machine):
    return (isinstance(machine,dict) and set(machine)=={"protocol","pocket","controller"}
            and machine["protocol"]==PROTOCOL and st43.verify(machine["pocket"])
            and st44.verify(machine["controller"],machine["pocket"]))

def transition(machine,action,payload=None):
    """Pure deterministic transition; never executes external tools or GitHub Actions."""
    if not verify(machine):raise ValueError("invalid machine state")
    if action not in TOOLS:raise ValueError("unknown action")
    payload={} if payload is None else payload
    if not isinstance(payload,dict):raise ValueError("payload must be object")
    ledger=machine["pocket"]
    controller=machine["controller"]
    if action=="inspect":
        return machine,{"verified":True,"enabled":controller["enabled"],
                        "records":len(ledger["events"]),"ticks":len(controller["ticks"])}
    if action=="recall":
        code=payload.get("code")
        if type(code) is not int:raise ValueError("integer code required")
        records=st43.lookup(ledger,code)
        return machine,{"matches":records}
    if action=="stop":
        controller=st44.stop(controller,ledger)
        return {"protocol":PROTOCOL,"pocket":ledger,"controller":controller},{"stopped":True}
    if not controller["enabled"]:raise ValueError("machine stopped")
    if action=="tick":
        controller=st44.step(controller,ledger)
        return {"protocol":PROTOCOL,"pocket":ledger,"controller":controller},{"ticks":len(controller["ticks"])}
    if action=="remember":
        # Pocket updates invalidate the previous binding. Explicitly start a new
        # controller epoch, preserving old ledger history and avoiding silent reuse.
        if controller["ticks"]:
            raise ValueError("memory update requires an idle controller epoch")
        record=st42.pocket_record(payload["name"],payload["values"],payload["message"])
        ledger=st43.append(ledger,record)
        controller=st44.genesis(ledger)
        return {"protocol":PROTOCOL,"pocket":ledger,"controller":controller},{"code":record["godel_number"]}
    raise AssertionError("unreachable")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--file",default="doraemon-g.json")
    parser.add_argument("--init",action="store_true")
    parser.add_argument("--action",choices=TOOLS,default="inspect")
    parser.add_argument("--payload",default="{}")
    args=parser.parse_args()
    path=Path(args.file)
    if args.init:
        if path.exists():raise SystemExit("Refusing to overwrite existing state")
        machine=initialize()
    else:
        if path.stat().st_size>st43.MAX_BYTES*2:raise SystemExit("oversize state")
        machine=json.loads(path.read_text(encoding="utf-8"))
    payload=json.loads(args.payload)
    next_state,result=transition(machine,args.action,payload)
    if not verify(next_state):raise SystemExit("postcondition failed")
    if args.init or next_state is not machine:
        import os,tempfile
        path.parent.mkdir(parents=True,exist_ok=True)
        fd,tmp=tempfile.mkstemp(prefix="."+path.name+".",dir=str(path.parent))
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                json.dump(next_state,f,ensure_ascii=False,indent=2)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    print(json.dumps({"result":result,"state_verified":True},ensure_ascii=False))

if __name__=="__main__":main()
