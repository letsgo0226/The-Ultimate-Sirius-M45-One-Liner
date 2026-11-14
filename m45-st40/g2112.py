#!/usr/bin/env python3
"""G-2112: exact prime-labelled symbolic operators and a fictional year bridge.

No physical particles, retrocausal communication, or autonomous network activity.
"""
import argparse
import hashlib
import json
from fractions import Fraction

def primes(n):
    if type(n) is not int or not 1<=n<=100:raise ValueError("n must be 1..100")
    result=[]
    candidate=2
    while len(result)<n:
        if all(candidate%p for p in result if p*p<=candidate):
            result.append(candidate)
        candidate+=1
    return result

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,str)):raise ValueError("use exact integer or fraction string")
    f=Fraction(x)
    if f.denominator>1000000 or abs(f.numerator)>1000000000:
        raise ValueError("coefficient out of bounds")
    return f

def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def digest(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

def state(n,coefficients):
    basis=primes(n)
    if len(coefficients)!=n:raise ValueError("wrong coefficient count")
    values=[rational(x) for x in coefficients]
    return {str(p):v for p,v in zip(basis,values)}

def apply(s,operation,amount=1):
    """Linear maps on a rational vector indexed by primes."""
    basis=list(s)
    v=[rational(s[p]) for p in basis]
    if operation=="identity":out=v
    elif operation=="rotate":out=v[-1:]+v[:-1]
    elif operation=="scale":out=[rational(amount)*x for x in v]
    elif operation=="difference":out=[v[i]-v[(i-1)%len(v)] for i in range(len(v))]
    else:raise ValueError("unsupported operator")
    return {p:str(x) for p,x in zip(basis,out)}

def norm2(s):
    return str(sum((rational(v)**2 for v in s.values()),Fraction(0)))

def bridge(message,source_year=2026,target_year=2112):
    if type(source_year) is not int or type(target_year) is not int:
        raise ValueError("years must be integers")
    if not 0<=source_year<=9999 or not 0<=target_year<=9999:
        raise ValueError("year out of range")
    if not isinstance(message,str) or len(message)>500:
        raise ValueError("message must be at most 500 characters")
    payload={"protocol":"G-2112-FICTIONAL-BRIDGE-v1","source_year":source_year,
             "target_year":target_year,"message":message,
             "semantics":"LOCAL_SIMULATED_MESSAGE_NO_TIME_TRAVEL"}
    return {**payload,"sha256":digest(payload)}

def experiment(n=5,operation="rotate",amount=1):
    initial=state(n,[1]+[0]*(n-1))
    final=apply(initial,operation,amount)
    payload={"protocol":"M45-ST40","basis":primes(n),
             "initial":{k:str(v) for k,v in initial.items()},
             "operator":operation,"amount":str(rational(amount)),
             "final":final,"norm2_initial":norm2(initial),"norm2_final":norm2(final),
             "bridge":bridge("2112 is a fictional narrative horizon; 2026 is the computation date.")}
    return {**payload,"sha256":digest(payload)}

def verify(record):
    if not isinstance(record,dict):return False
    try:
        body=dict(record)
        sha=body.pop("sha256")
        if digest(body)!=sha or body["protocol"]!="M45-ST40":return False
        basis=body["basis"]
        if basis!=primes(len(basis)):return False
        expected=experiment(len(basis),body["operator"],body["amount"])
        return expected==record
    except (ValueError,KeyError,TypeError,ZeroDivisionError,OverflowError):
        return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--primes",type=int,default=5)
    p.add_argument("--operator",choices=("identity","rotate","scale","difference"),default="rotate")
    p.add_argument("--amount",default="1")
    p.add_argument("--out",default="m45-st40-certificate.json")
    a=p.parse_args()
    record=experiment(a.primes,a.operator,a.amount)
    assert verify(record)
    with open(a.out,"w",encoding="utf-8") as f:
        json.dump(record,f,indent=2,ensure_ascii=False)
        f.write("\n")
    print(canonical({"verified":True,"final":record["final"],"norm2_final":record["norm2_final"]}))

if __name__=="__main__":main()
