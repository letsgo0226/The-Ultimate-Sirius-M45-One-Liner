#!/usr/bin/env python3
"""ST61: exact observer-frame invariants for real-qubit Bloch states.

Frame words H,Z are orthogonal signed-permutation transformations on (x,z).
An observer transforms both state coordinates and measurement axes. The
invariant is the Born expectation, not an individual stochastic outcome.
"""
import argparse
import json
from fractions import Fraction

H=((0,1),(1,0))
Z=((-1,0),(0,1))
I=((1,0),(0,1))
AXES={"X":(1,0),"Z":(0,1)}

def dot(a,b):
    return sum(u*v for u,v in zip(a,b))

def apply(matrix,vector):
    return tuple(dot(row,vector) for row in matrix)

def compose(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))

def operator(word):
    if not isinstance(word,str) or len(word)>64 or any(c not in "HZ" for c in word):
        raise ValueError("word must be a string of H and Z of length <=64")
    result=I
    for letter in word:
        result=compose(H if letter=="H" else Z,result)
    return result

def rational(value):
    if isinstance(value,bool):
        raise ValueError("boolean is not a rational coordinate")
    try:
        f=Fraction(value)
    except (TypeError,ValueError,ZeroDivisionError,OverflowError):
        raise ValueError("invalid rational coordinate") from None
    if f.denominator>1000000 or abs(f.numerator)>1000000:
        raise ValueError("rational coordinate exceeds bounds")
    return f

def state(x,z):
    x,z=rational(x),rational(z)
    if x*x+z*z>1:
        raise ValueError("state outside real Bloch disk")
    return (x,z)

def probabilities(s,axis):
    e=dot(s,axis)
    return ((1+e)/2,(1-e)/2)

def analyze(x="3/5",z="4/5",word="HZ",axis="Z",flip="0"):
    s=state(x,z)
    if axis not in AXES:
        raise ValueError("axis must be X or Z")
    flip=rational(flip)
    if not 0<=flip< Fraction(1,2):
        raise ValueError("symmetric detector flip must be in [0,1/2)")
    transform=operator(word)
    new_state=apply(transform,s)
    original_axis=AXES[axis]
    new_axis=apply(transform,original_axis)
    reference=probabilities(s,original_axis)
    transformed=probabilities(new_state,new_axis)
    if reference!=transformed:
        raise AssertionError("covariance failed")
    purity=(1+dot(s,s))/2
    determinant=(1-dot(s,s))/4
    measured_expectation=(1-2*flip)*dot(new_state,new_axis)
    calibrated_expectation=measured_expectation/(1-2*flip)
    if calibrated_expectation!=dot(s,original_axis):
        raise AssertionError("calibration failed")
    encode=lambda v: str(v)
    return {
        "protocol":"M45-ST61-OBSERVER-INDEPENDENT-INVARIANTS-v1",
        "state_bloch_xz":[encode(v) for v in s],
        "frame_word":word,
        "frame_matrix":[list(row) for row in transform],
        "transformed_state":[encode(v) for v in new_state],
        "reference_axis":axis,
        "transformed_axis":list(new_axis),
        "reference_born_plus":encode(reference[0]),
        "transformed_born_plus":encode(transformed[0]),
        "detector_flip_probability":encode(flip),
        "measured_expectation":encode(measured_expectation),
        "calibrated_expectation":encode(calibrated_expectation),
        "frame_invariant_trace":"1",
        "frame_invariant_purity":encode(purity),
        "frame_invariant_determinant":encode(determinant),
        "covariant_probability_equal":reference==transformed,
        "interpretation":"EXACT_RATIONAL_FRAME_COVARIANCE_NOT_EQUAL_INDIVIDUAL_OUTCOMES"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--x",default="3/5")
    ap.add_argument("--z",default="4/5")
    ap.add_argument("--word",default="HZ")
    ap.add_argument("--axis",default="Z")
    ap.add_argument("--flip",default="0")
    args=ap.parse_args()
    print(json.dumps(analyze(args.x,args.z,args.word,args.axis,args.flip),
                     indent=2,sort_keys=True))
if __name__=="__main__":main()
