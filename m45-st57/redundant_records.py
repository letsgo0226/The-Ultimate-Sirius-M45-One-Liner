#!/usr/bin/env python3
"""ST57: classical information in redundant environment records.

A pointer bit S ~ Bernoulli(p) is independently copied into m environment
record bits through a binary symmetric channel with error q. The resulting
classical mutual information is a toy diagnostic of redundant accessibility,
not a full quantum Darwinism proof or a quantum many-body simulation.
"""
import argparse
import json
import math

def validate(n,p,q,delta):
    if isinstance(n,bool) or not isinstance(n,int) or not 1<=n<=64:
        raise ValueError("n must be integer in 1..64")
    for name,v,hi in (("p",p,1),("q",q,0.5),("delta",delta,1)):
        if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or not 0<=v<=hi:
            raise ValueError(name+" outside allowed range")

def h2(p):
    if p<=0 or p>=1:return 0.0
    return -p*math.log2(p)-(1-p)*math.log2(1-p)

def binomial(n,k,p):
    if p==0:return 1.0 if k==0 else 0.0
    if p==1:return 1.0 if k==n else 0.0
    return math.comb(n,k)*(p**k)*((1-p)**(n-k))

def information(m,p,q):
    """I(S;F_m) in bits using sufficient statistic K=#ones in fragment."""
    prior=h2(p)
    conditional=0.0
    for k in range(m+1):
        likelihood_s1=binomial(m,k,1-q)
        likelihood_s0=binomial(m,k,q)
        joint1=p*likelihood_s1
        joint0=(1-p)*likelihood_s0
        mass=joint1+joint0
        if mass:
            conditional+=mass*h2(joint1/mass)
    return max(0.0,min(prior,prior-conditional))

def analyze(n=12,p=0.5,q=0.1,delta=0.1):
    validate(n,p,q,delta)
    plateau=h2(p)
    curve=[information(m,p,q) for m in range(n+1)]
    target=(1-delta)*plateau
    # If H(S)=0, information about S is trivially zero: no meaningful redundancy.
    first=next((m for m in range(1,n+1) if curve[m]+1e-12>=target),None) if plateau>0 else None
    redundancy=(n//first) if first is not None else None
    return {
        "protocol":"M45-ST57-REDUNDANT-RECORDS-v1",
        "assumptions":["classical pointer bit S","conditionally independent noisy record fragments",
                       "binary symmetric channel error q","accessible classical mutual information"],
        "parameters":{"n":n,"p":p,"q":q,"delta":delta},
        "pointer_entropy_bits":plateau,
        "fragment_information_bits":curve,
        "target_information_bits":target,
        "minimum_fragment_size_for_target":first,
        "disjoint_fragment_redundancy_lower_bound":redundancy,
        "interpretation":"CLASSICAL_REDUNDANT_RECORD_TOY_MODEL_NOT_FULL_QUANTUM_DARWINISM"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=12)
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--q",type=float,default=0.1)
    ap.add_argument("--delta",type=float,default=0.1)
    a=ap.parse_args()
    print(json.dumps(analyze(a.n,a.p,a.q,a.delta),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
