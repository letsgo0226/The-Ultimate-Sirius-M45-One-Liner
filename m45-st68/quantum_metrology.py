#!/usr/bin/env python3
"""ST68: pure-state quantum Fisher information in finite Z2 relational frames.

Parameter encoding: exp(-i theta X_v/2) on A-frame second relational qubit.
In B coordinates, both state and generator are transported by the ST64
unitary frame permutation. QFI = 4 Var(G), G=X_v/2.
"""
import argparse
import cmath
import importlib.util
import json
import math
from pathlib import Path

def load_st64():
    path=Path(__file__).resolve().parent.parent/"m45-st64"/"frame_switch.py"
    spec=importlib.util.spec_from_file_location("st64_frame_switch",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def x_second(psi):
    return (psi[1],psi[0],psi[3],psi[2])

def inner(a,b):
    return sum(x.conjugate()*y for x,y in zip(a,b))

def encode(psi,theta):
    c=math.cos(theta/2)
    s=math.sin(theta/2)
    xpsi=x_second(psi)
    return tuple(c*z-1j*s*x for z,x in zip(psi,xpsi))

def qfi(psi):
    # X_v^2=I and G=X_v/2.
    expectation=inner(psi,x_second(psi)).real
    return max(0.0,1-expectation**2)

def event_probability(psi,frame):
    return sum(abs(psi[2*u+v])**2 for u in range(2) for v in range(2)
               if (u==v if frame=="A" else v==0))

def classical_fi(psi,theta,st64):
    # Analytic derivative d|psi_theta>/dtheta = -i X_v|psi_theta>/2.
    state=encode(psi,theta)
    derivative=tuple(-0.5j*z for z in x_second(state))
    p=event_probability(state,"A")
    dp=2*sum((state[2*u+v].conjugate()*derivative[2*u+v]).real
             for u in range(2) for v in range(2) if u==v)
    if p<=1e-12 or p>=1-1e-12:
        return {"probability":p,"derivative":dp,"fisher_information":None,
                "note":"binary FI not evaluated at boundary probability"}
    return {"probability":p,"derivative":dp,"fisher_information":dp*dp/(p*(1-p)),
            "note":"regular binary measurement"}

def analyze(amplitudes=("1","1j","0","0"),theta=0.3):
    if isinstance(theta,bool) or not isinstance(theta,(int,float)) or not math.isfinite(theta) or abs(theta)>1e6:
        raise ValueError("theta must be finite and bounded")
    st64=load_st64()
    a=st64.normalize(amplitudes)
    b=st64.switch_a_to_b(a)
    a_theta=encode(a,theta)
    # Transport the encoding, not merely the state: U exp(-i theta G) U^dagger.
    b_theta=st64.switch_a_to_b(a_theta)
    b_generator_on_state=st64.switch_a_to_b(x_second(a))
    qfi_a=qfi(a)
    transported_x_expectation=inner(b,b_generator_on_state).real
    qfi_b=max(0.0,1-transported_x_expectation**2)
    measured=classical_fi(a,theta,st64)
    p_a=measured["probability"]
    p_b=event_probability(b_theta,"B")
    error=max(abs(qfi_a-qfi_b),abs(p_a-p_b))
    if error>1e-10:raise AssertionError("metrology frame covariance failed")
    if measured["fisher_information"] is not None and measured["fisher_information"]>qfi_a+1e-10:
        raise AssertionError("classical Fisher information exceeds quantum Fisher information")
    return {
        "protocol":"M45-ST68-RELATIONAL-QUANTUM-METROLOGY-v1",
        "parameter_theta_radians":theta,
        "generator_a":"X_on_second_relational_qubit_over_2",
        "generator_b":"U_frame_G_a_U_frame_dagger",
        "a_frame_quantum_fisher_information":qfi_a,
        "b_frame_quantum_fisher_information":qfi_b,
        "binary_relational_measurement":measured,
        "b_frame_binary_event_probability":p_b,
        "single_copy_quantum_cramer_rao_variance_bound":None if qfi_a<=1e-12 else 1/qfi_a,
        "max_frame_invariant_error":error,
        "interpretation":"LOCAL_PURE_STATE_QFI_BOUND_NOT_GUARANTEED_FINITE_SAMPLE_ESTIMATION"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--amplitudes",nargs=4,default=["1","1j","0","0"])
    ap.add_argument("--theta",type=float,default=0.3)
    args=ap.parse_args()
    print(json.dumps(analyze(args.amplitudes,args.theta),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
