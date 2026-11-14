#!/usr/bin/env python3
"""ST49: finite-dimensional quantum dephasing, NOT physical collapse."""
import argparse
import json
import math

TOL=1e-10

def state(p=0.5,coherence=1.0):
    """Density matrix of a qubit with real coherence in the Z basis."""
    if not all(isinstance(x,(float,int)) and math.isfinite(x) for x in (p,coherence)):
        raise ValueError("parameters must be finite numbers")
    if not 0<=p<=1 or not 0<=coherence<=1:
        raise ValueError("p and coherence must be in [0,1]")
    off=coherence*math.sqrt(p*(1-p))
    return [[p,off],[off,1-p]]

def dephase(rho,gamma):
    """Phase-damping CPTP map: off-diagonals multiplied by gamma."""
    if not isinstance(gamma,(float,int)) or not math.isfinite(gamma) or not 0<=gamma<=1:
        raise ValueError("gamma must be in [0,1]")
    validate(rho)
    out=[[rho[0][0],rho[0][1]*gamma],
         [rho[1][0]*gamma,rho[1][1]]]
    validate(out)
    return out

def validate(rho):
    if not isinstance(rho,list) or len(rho)!=2 or any(not isinstance(r,list) or len(r)!=2 for r in rho):
        raise ValueError("expected 2x2 density matrix")
    if any(not isinstance(v,(int,float,complex)) or not math.isfinite(v.real) or not math.isfinite(v.imag)
           for row in rho for v in row):
        raise ValueError("nonfinite or nonnumeric entry")
    a,b=rho[0];c,d=rho[1]
    if abs(a.imag)>TOL or abs(d.imag)>TOL or abs(a+d-1)>TOL or abs(b-c.conjugate())>TOL:
        raise ValueError("not Hermitian or trace-one")
    if a.real < -TOL or d.real < -TOL or a.real*d.real-abs(b)**2 < -TOL:
        raise ValueError("matrix not positive semidefinite")
    return True

def measure(rho,basis):
    """Born probabilities for Z or X projective measurement, no sampling."""
    validate(rho)
    if basis=="Z":
        plus=rho[0][0].real
    elif basis=="X":
        plus=0.5+(rho[0][1]+rho[1][0]).real/2
    else:
        raise ValueError("basis must be X or Z")
    if not -TOL<=plus<=1+TOL:raise ValueError("invalid probability")
    plus=min(1.0,max(0.0,plus))
    return {"plus":plus,"minus":1-plus}

def experiment(p,gamma):
    initial=state(p,1.0)
    final=dephase(initial,gamma)
    return {"protocol":"M45-ST49-DEPHASING-v1",
            "interpretation":"SIMULATION_NOT_PHYSICAL_COLLAPSE",
            "parameters":{"p":p,"gamma":gamma},
            "initial":{"Z":measure(initial,"Z"),"X":measure(initial,"X")},
            "final":{"Z":measure(final,"Z"),"X":measure(final,"X")},
            "density_matrix":[[float(v.real) for v in row] for row in final],
            "coherence_l1":2*abs(final[0][1])}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--gamma",type=float,default=0.0)
    args=ap.parse_args()
    print(json.dumps(experiment(args.p,args.gamma),sort_keys=True,indent=2,allow_nan=False))
if __name__=="__main__":main()
