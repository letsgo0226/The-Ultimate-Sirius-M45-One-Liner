#!/usr/bin/env python3
"""ST56: explicit system-environment entanglement and partial trace.

A system qubit controls a real rotation of a single environment qubit.
The joint state remains pure; the reduced system can become mixed.
"""
import argparse
import json
import math

def finite_unit_interval(name,value):
    if not isinstance(value,(int,float)) or not math.isfinite(value) or not 0<=value<=1:
        raise ValueError(name+" must be finite in [0,1]")

def von_neumann_entropy(rho):
    a,b=rho[0]
    _,d=rho[1]
    discriminant=max(0.0,(a-d)**2+4*b*b)
    eigenvalues=((1+math.sqrt(discriminant))/2,(1-math.sqrt(discriminant))/2)
    return -sum(v*math.log2(v) for v in eigenvalues if v>1e-15)

def analyze(p=0.5,theta=math.pi/2):
    finite_unit_interval("p",p)
    if not isinstance(theta,(int,float)) or not math.isfinite(theta) or not 0<=theta<=math.pi/2:
        raise ValueError("theta must be finite in [0,pi/2]")
    # Joint amplitudes indexed [system][environment]:
    # sqrt(p)|00> + sqrt(1-p)cos(theta)|10> + sqrt(1-p)sin(theta)|11>
    a=math.sqrt(p)
    b=math.sqrt(1-p)
    joint=[[a,0.0],[b*math.cos(theta),b*math.sin(theta)]]
    # Tr_E |psi><psi|: rho_S[s,t] = sum_e joint[s,e]*joint[t,e].
    reduced=[[math.fsum(joint[s][e]*joint[t][e] for e in range(2))
              for t in range(2)] for s in range(2)]
    purity=math.fsum(reduced[s][t]**2 for s in range(2) for t in range(2))
    norm=math.fsum(v*v for row in joint for v in row)
    gamma=math.cos(theta)
    expected=[[p,math.sqrt(p*(1-p))*gamma],
              [math.sqrt(p*(1-p))*gamma,1-p]]
    max_error=max(abs(reduced[s][t]-expected[s][t]) for s in range(2) for t in range(2))
    if abs(norm-1)>1e-12 or max_error>1e-12:
        raise AssertionError("normalization or partial trace failed")
    return {
        "protocol":"M45-ST56-ENVIRONMENT-INDUCED-DECOHERENCE-v1",
        "parameters":{"p":p,"theta_radians":theta},
        "joint_amplitudes":joint,
        "joint_purity":1.0,
        "reduced_density_matrix":reduced,
        "reduced_purity":purity,
        "reduced_von_neumann_entropy_bits":von_neumann_entropy(reduced),
        "environment_overlap_gamma":gamma,
        "reduced_coherence_l1":2*abs(reduced[0][1]),
        "max_error_vs_st49_phase_damping":max_error,
        "interpretation":"UNITARY_ENTANGLEMENT_AND_PARTIAL_TRACE_NOT_OBJECTIVE_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--theta",type=float,default=math.pi/2)
    args=ap.parse_args()
    print(json.dumps(analyze(args.p,args.theta),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
