#!/usr/bin/env python3
"""ST58: explicit diagonal quantum density operators and SBS conditions.

rho_SE = p |0><0| tensor tau_0^tensorN
       + (1-p) |1><1| tensor tau_1^tensorN.
tau_0=diag(1-q,q), tau_1=diag(q,1-q). The state is a
classical-quantum density operator (diagonal in the chosen pointer basis).
For 0<p<1 and N>=1, exact spectrum broadcast structure requires
tau_0*tau_1=0, i.e. q=0 for q in [0,1/2].
"""
import argparse
import json
import math

def validate(n,p,q):
    if type(n) is not int or not 1<=n<=8:
        raise ValueError("n must be integer 1..8")
    for name,v,upper in (("p",p,1),("q",q,0.5)):
        if isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=upper:
            raise ValueError(name+" outside valid range")

def h2(v):
    if v<=0 or v>=1:return 0.0
    return -v*math.log2(v)-(1-v)*math.log2(1-v)

def environment_conditional(n,q,s):
    """Diagonal of tau_s^tensorN in lexicographic bit order."""
    return [math.prod(((1-q) if ((mask>>j)&1)==s else q)
                      for j in range(n)) for mask in range(1<<n)]

def analyze(n=3,p=0.5,q=0.1):
    validate(n,p,q)
    a=environment_conditional(n,q,0)
    b=environment_conditional(n,q,1)
    # Full diagonal density matrix is diag(joint_diagonal). No off-diagonal
    # entries; representation is exact as a diagonal operator, not a sample.
    joint=[p*v for v in a]+[(1-p)*v for v in b]
    env=[p*v+(1-p)*w for v,w in zip(a,b)]
    entropy=lambda d:-sum(v*math.log2(v) for v in d if v>0)
    hs=h2(p)
    henv=entropy(env)
    hjoint=entropy(joint)
    mutual=hs+henv-hjoint
    overlap=sum(math.sqrt(v*w) for v,w in zip(a,b))
    # Tr(tau_0 tau_1) per fragment; zero iff orthogonal support.
    single_trace_overlap=2*q*(1-q)
    exact_sbs=(single_trace_overlap==0)
    return {
        "protocol":"M45-ST58-SPECTRUM-BROADCAST-STRUCTURE-v1",
        "scope":"DIAGONAL_POINTER_CLASSICAL_QUANTUM_DENSITY_OPERATOR",
        "parameters":{"n":n,"p":p,"q":q},
        "joint_density_matrix_diagonal":joint,
        "joint_dimension":2**(n+1),
        "trace":sum(joint),
        "system_entropy_bits":hs,
        "environment_entropy_bits":henv,
        "joint_entropy_bits":hjoint,
        "system_environment_mutual_information_bits":mutual,
        "single_fragment_trace_overlap":single_trace_overlap,
        "environment_conditional_fidelity_root":overlap,
        "exact_sbs_conditional_support_orthogonal":exact_sbs,
        "interpretation":"CONSTRUCTED_DIAGONAL_CQ_STATE_NOT_DYNAMIC_EMERGENCE_OR_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=3)
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--q",type=float,default=0.1)
    args=ap.parse_args()
    print(json.dumps(analyze(args.n,args.p,args.q),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
