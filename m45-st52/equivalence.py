#!/usr/bin/env python3
"""ST52: exact observational equivalence classes on a finite qubit grid.

Grid states are labelled by (p, coherence). Equality is based on exact
rational probabilities, not floating-point tolerance or hidden ontology.
"""
import argparse
from fractions import Fraction
import json

def validate_grid(denominator):
    if not isinstance(denominator,int) or isinstance(denominator,bool) or not 1<=denominator<=32:
        raise ValueError("denominator must be integer 1..32")

def grid(denominator=4):
    validate_grid(denominator)
    # rho = [[p,c],[c,1-p]] with c real and |c| <= sqrt(p(1-p)).
    # Discrete rational grid is intentionally limited to nonnegative c.
    states=[]
    for i in range(denominator+1):
        p=Fraction(i,denominator)
        for j in range(denominator+1):
            c=Fraction(j,denominator)
            if c*c<=p*(1-p):
                states.append((p,c))
    return states

def probability(state,context):
    p,c=state
    if context=="Z":return p
    if context=="X":return Fraction(1,2)+c
    if context=="XZ":return (p,Fraction(1,2)+c)
    raise ValueError("context must be Z, X or XZ")

def classes(denominator=4,context="Z"):
    states=grid(denominator)
    if context not in ("Z","X","XZ"):raise ValueError("unknown context")
    groups={}
    for state in states:
        key=probability(state,context)
        groups.setdefault(key,[]).append(state)
    return groups

def fstr(value):
    if isinstance(value,tuple):return [fstr(v) for v in value]
    return str(value)

def report(denominator=4):
    states=grid(denominator)
    result={"protocol":"M45-ST52-OBSERVATIONAL-EQUIVALENCE-v1",
            "scope":"FINITE_RATIONAL_REAL_QUBIT_DENSITY_MATRICES",
            "denominator":denominator,"state_count":len(states),"contexts":{}}
    for context in ("Z","X","XZ"):
        groups=classes(denominator,context)
        result["contexts"][context]={
            "class_count":len(groups),
            "largest_class_size":max(map(len,groups.values())),
            "classes":[{"probability":fstr(key),
                        "states":[{"p":str(p),"c":str(c)} for p,c in members]}
                       for key,members in sorted(groups.items())]}
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--denominator",type=int,default=4)
    args=ap.parse_args()
    print(json.dumps(report(args.denominator),indent=2,ensure_ascii=False))
if __name__=="__main__":main()
