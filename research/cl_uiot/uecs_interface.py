"""Independent offline UECS interface; no baseline changes."""
import json
from fractions import Fraction as Q
from symbolic_algebra import decode_expr,normalize
from proof_halting import run,verify
from operator_calculus import evaluate,verify as verify_operator
from correspondence import produce
from certificate_codec import encode,decode
from algebraic_zero import roots

def identity_request(ga,gb):
    try:
        a,b=decode_expr(ga),decode_expr(gb)
        r=run(a,b)
        if not verify(r,a,b):
            return {"state":"UNKNOWN"}
        c=r[3]
        energy=sum((v*v for v in c),Q(0))
        return {"state":r[0],"certificate":r,"energy":energy,
                "zeros":roots(energy),"verified":True}
    except (ValueError,TypeError,OverflowError,RecursionError):
        return {"state":"UNKNOWN"}

def operator_request(g,t):
    try:
        e=decode_expr(g)
        r=evaluate(e,t)
        if verify_operator(e,t,r):
            return {"state":"VERIFIED_RESULT","matrix":r,"verified":True}
    except (ValueError,TypeError,OverflowError,RecursionError):
        pass
    return {"state":"UNKNOWN"}

def correspondence_request(l,m):
    try:
        c=produce(l,m)
        g=encode(c)
        if decode(g)==c:
            return {"state":c["state"],"certificate_code":g,"verified":True}
    except (ValueError,TypeError,OverflowError,RecursionError):
        pass
    return {"state":"UNKNOWN"}

def wire(v):
    if type(v) is Q:
        return {"numerator":hex(v.numerator),"denominator":hex(v.denominator)}
    if type(v) is int:
        return {"integer":hex(v)}
    if type(v) is tuple:
        return [wire(x) for x in v]
    if type(v) is dict:
        return {k:wire(x) for k,x in v.items()}
    if v is None or type(v) in (str,bool):
        return v
    raise ValueError("unsupported output")

def report(result):
    return json.dumps(wire(result),sort_keys=True,separators=(",",":"))
