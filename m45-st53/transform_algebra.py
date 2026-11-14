#!/usr/bin/env python3
"""ST53: exact rational Bloch-plane transformations and measurement covariance.

H and Z are *state transformations* (unitary conjugations), not arbitrary
renamings of measurement devices. The corresponding transformed measurement
context is explicitly tracked.
"""
import argparse
from fractions import Fraction
import json

I=((1,0),(0,1))
H=((0,1),(1,0))  # conjugation by Hadamard: (x,z) -> (z,x)
Z=((-1,0),(0,1)) # conjugation by Pauli Z: (x,z) -> (-x,z)
GENERATORS={"H":H,"Z":Z}

def compose(a,b):
    """a after b, on Bloch column (x,z)."""
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))

def inverse(a):
    return tuple(tuple(a[j][i] for j in range(2)) for i in range(2))

def operator(word):
    if not isinstance(word,str) or len(word)>64 or any(c not in GENERATORS for c in word):
        raise ValueError("word must contain at most 64 H/Z generators")
    op=I
    for letter in word:
        op=compose(GENERATORS[letter],op)
    return op

def state(x,z):
    x,z=Fraction(x),Fraction(z)
    if x*x+z*z>1:raise ValueError("outside Bloch disk")
    return (x,z)

def transform(op,s):
    x,z=s
    return (op[0][0]*x+op[0][1]*z,op[1][0]*x+op[1][1]*z)

def probability(s,axis):
    if axis not in ("X","Z"):raise ValueError("axis must be X or Z")
    return (1+(s[0] if axis=="X" else s[1]))/2

def measured_axis(op,axis):
    """Return input-frame signed axis for measuring axis after op."""
    row=op[0] if axis=="X" else op[1]
    if row==(1,0):return "+X"
    if row==(-1,0):return "-X"
    if row==(0,1):return "+Z"
    if row==(0,-1):return "-Z"
    raise ValueError("unsupported measurement axis")

def original_probability(s,signed_axis):
    sign=1 if signed_axis[0]=="+" else -1
    axis=signed_axis[1]
    return (1+sign*(s[0] if axis=="X" else s[1]))/2

def report(x="3/5",z="4/5",word="HZ"):
    s=state(x,z)
    op=operator(word)
    after=transform(op,s)
    contexts={}
    for axis in ("X","Z"):
        transformed_context=measured_axis(op,axis)
        lhs=probability(after,axis)
        rhs=original_probability(s,transformed_context)
        contexts[axis]={"transformed_input_context":transformed_context,
                        "probability_after":str(lhs),
                        "probability_before_in_transformed_context":str(rhs),
                        "covariant":lhs==rhs}
    return {"protocol":"M45-ST53-OBSERVATIONAL-TRANSFORMS-v1",
            "scope":"REAL_QUBIT_BLOCH_DISK_H_Z_CONJUGATIONS",
            "initial":{"x":str(s[0]),"z":str(s[1])},
            "word":word,"operator":op,
            "final":{"x":str(after[0]),"z":str(after[1])},
            "contexts":contexts,
            "interpretation":"FINITE_OPERATOR_ALGEBRA_NOT_PHYSICAL_UNIVERSE_CONTROL"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--x",default="3/5")
    ap.add_argument("--z",default="4/5")
    ap.add_argument("--word",default="HZ")
    args=ap.parse_args()
    print(json.dumps(report(args.x,args.z,args.word),indent=2,sort_keys=True))
if __name__=="__main__":main()
