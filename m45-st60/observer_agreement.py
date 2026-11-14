#!/usr/bin/env python3
"""ST60: observer agreement for disjoint, conditionally independent records.

Each observer reads an odd number m of noisy copies of a latent pointer bit S,
and decides by majority vote. Given S, records and observer errors are
independent. Agreement is not equated with truth or physical objectivity.
"""
import argparse
import json
import math

def validate(n,m,p,q,accuracy_threshold,agreement_threshold):
    if type(n) is not int or not 2<=n<=128:
        raise ValueError("n must be integer 2..128")
    if type(m) is not int or not 1<=m<=n//2 or m%2!=1:
        raise ValueError("m must be odd integer 1..floor(n/2)")
    for name,v,lo,hi in (("p",p,0,1),("q",q,0,0.5),
                         ("accuracy_threshold",accuracy_threshold,0,1),
                         ("agreement_threshold",agreement_threshold,0,1)):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not lo<=v<=hi:
            raise ValueError(name+" outside valid range")

def majority_error(m,q):
    if q==0:return 0.0
    if q==0.5:return 0.5
    return math.fsum(math.comb(m,k)*q**k*(1-q)**(m-k)
                     for k in range((m+1)//2,m+1))

def analyze(n=24,m=3,p=0.5,q=0.1,accuracy_threshold=0.95,agreement_threshold=0.95):
    validate(n,m,p,q,accuracy_threshold,agreement_threshold)
    observers=n//m
    e=majority_error(m,q)
    accuracy=1-e
    agreement=(1-e)**2+e**2
    # All observers are correct conditional on S; conditional independence.
    all_correct=accuracy**observers
    # All observers agree, either all correct or all wrong.
    unanimous=accuracy**observers+e**observers
    return {
        "protocol":"M45-ST60-OBSERVER-AGREEMENT-v1",
        "assumptions":["latent classical pointer bit","disjoint record groups",
                       "conditionally independent binary symmetric channel noise",
                       "odd-sized majority vote","no observer communication"],
        "parameters":{"n":n,"m":m,"p":p,"q":q,
                      "accuracy_threshold":accuracy_threshold,
                      "agreement_threshold":agreement_threshold},
        "observer_count":observers,
        "unused_environment_records":n-observers*m,
        "per_observer_majority_error":e,
        "per_observer_truth_accuracy":accuracy,
        "pairwise_agreement_probability":agreement,
        "all_observers_correct_probability":all_correct,
        "unanimous_agreement_probability":unanimous,
        "criteria":{"accuracy_pass":accuracy>=accuracy_threshold,
                    "agreement_pass":agreement>=agreement_threshold,
                    "operational_objectivity":accuracy>=accuracy_threshold and agreement>=agreement_threshold},
        "interpretation":"THRESHOLD_DEPENDENT_CLASSICAL_AGREEMENT_NOT_OBJECTIVE_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=24)
    ap.add_argument("--m",type=int,default=3)
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--q",type=float,default=0.1)
    ap.add_argument("--accuracy-threshold",type=float,default=0.95)
    ap.add_argument("--agreement-threshold",type=float,default=0.95)
    a=ap.parse_args()
    print(json.dumps(analyze(a.n,a.m,a.p,a.q,a.accuracy_threshold,
                             a.agreement_threshold),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
