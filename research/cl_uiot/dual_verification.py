"""Fail-closed dual verification for bounded polynomial identities."""
from proof_halting import run,verify
from independent_identity import decide,compile_expr

def verify_dual(record,a,b):
    try:
        if not verify(record,a,b):
            return False
        second=decide(a,b)
        if second[0]!=record[0]:
            return False
        if record[0]=="HALT_PROOF":
            return True
        if record[0]=="HALT_COUNTEREXAMPLE":
            x,y=record[4]
            _,fa=compile_expr(a)
            _,fb=compile_expr(b)
            return y!=0 and fa(x)-fb(x)==y
        return False
    except (ValueError,TypeError,OverflowError,RecursionError):
        return False

def run_dual(a,b):
    r=run(a,b)
    if verify_dual(r,a,b):
        return {"state":r[0],"certificate":r,"dual_verified":True}
    return {"state":"UNKNOWN","dual_verified":False}
