#!/usr/bin/env python3
"""ST59: dynamically generated branching state and reduced-fragment SBS tests.

Each environment qubit begins |0>. Controlled rotation conditioned on the
system pointer |1> yields |e1>=cos(theta)|0>+sin(theta)|1>, while |0>
leaves |e0>=|0>. After N interactions the *global* state is pure:
sqrt(p)|0>|e0>^N + sqrt(1-p)|1>|e1>^N.

Tracing out N-m environment qubits suppresses the off-diagonal block of
rho_(S,F_m) by cos(theta)^(N-m). Exact SBS for a proper fragment requires
both zero cross block and orthogonal conditional single-fragment supports.
"""
import argparse
import json
import math

def validate(n,p,theta):
    if type(n) is not int or not 1<=n<=12:
        raise ValueError("n must be integer 1..12")
    if isinstance(p,bool) or not isinstance(p,(float,int)) or not math.isfinite(p) or not 0<p<1:
        raise ValueError("p must be finite and strictly between 0 and 1")
    if isinstance(theta,bool) or not isinstance(theta,(float,int)) or not math.isfinite(theta) or not 0<=theta<=math.pi/2:
        raise ValueError("theta must be finite in [0,pi/2]")

def analyze(n=4,p=0.5,theta=math.pi/2):
    validate(n,p,theta)
    overlap=max(0.0,math.cos(theta))
    # cos(pi/2) is not exactly zero in floating point; use a documented
    # tolerance for the orthogonal-endpoint classification.
    orthogonal=abs(theta-math.pi/2)<=1e-12
    records=[]
    for m in range(n+1):
        remainder=n-m
        factor=overlap**remainder
        # 1-norm of the off-diagonal S block, summed with its adjoint:
        # 2 sqrt(p(1-p)) |<e0|e1>|^(N-m).
        cross_norm=2*math.sqrt(p*(1-p))*factor
        # At m=0, the environment fragment is empty and cannot broadcast.
        conditional_fragment_overlap=overlap**m
        exact_sbs=(1<=m<n and orthogonal)
        records.append({
            "observed_environment_qubits":m,
            "traced_out_environment_qubits":remainder,
            "off_diagonal_block_trace_norm":cross_norm,
            "conditional_fragment_overlap":conditional_fragment_overlap,
            "exact_sbs_for_observed_fragment":exact_sbs
        })
    return {
        "protocol":"M45-ST59-DYNAMICAL-SPECTRUM-BROADCASTING-v1",
        "parameters":{"n":n,"p":p,"theta_radians":theta},
        "global_state_pure":True,
        "single_record_state_overlap":overlap,
        "system_reduced_coherence_l1":2*math.sqrt(p*(1-p))*overlap**n,
        "single_record_orthogonal_endpoint":orthogonal,
        "fragment_diagnostics":records,
        "interpretation":"CONTROLLED_UNITARY_BRANCHING_AND_PARTIAL_TRACE_NOT_COLLAPSE"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--n",type=int,default=4)
    ap.add_argument("--p",type=float,default=0.5)
    ap.add_argument("--theta",type=float,default=math.pi/2)
    a=ap.parse_args()
    print(json.dumps(analyze(a.n,a.p,a.theta),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
