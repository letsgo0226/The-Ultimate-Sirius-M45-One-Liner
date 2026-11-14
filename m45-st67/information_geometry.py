#!/usr/bin/env python3
"""ST67: pure-state relational information geometry under finite Z2 frame switches.

For normalized relational pure states psi and phi, the frame switch from
ST64 is a common unitary permutation. Their transition fidelity, pure-state
trace distance, Fubini-Study angle, and Bures distance are invariant.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

def load_st64():
    path=Path(__file__).resolve().parent.parent/"m45-st64"/"frame_switch.py"
    spec=importlib.util.spec_from_file_location("st64_frame_switch",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def inner(psi,phi):
    return sum(a.conjugate()*b for a,b in zip(psi,phi))

def geometry(psi,phi):
    fidelity=min(1.0,max(0.0,abs(inner(psi,phi))**2))
    return {
        "fidelity":fidelity,
        "trace_distance":math.sqrt(max(0.0,1-fidelity)),
        "fubini_study_angle_radians":math.acos(math.sqrt(fidelity)),
        "bures_distance":math.sqrt(max(0.0,2*(1-math.sqrt(fidelity))))
    }

def event_probability(psi,frame):
    # ST64 relational event B=C in either coordinate system.
    return sum(abs(psi[2*u+v])**2 for u in range(2) for v in range(2)
               if (u==v if frame=="A" else v==0))

def analyze(first=("1","0","1","0"),second=("1","0","0","1")):
    st64=load_st64()
    psi=st64.normalize(first)
    phi=st64.normalize(second)
    switched_psi=st64.switch_a_to_b(psi)
    switched_phi=st64.switch_a_to_b(phi)
    a=geometry(psi,phi)
    b=geometry(switched_psi,switched_phi)
    p_psi_a=event_probability(psi,"A")
    p_phi_a=event_probability(phi,"A")
    p_psi_b=event_probability(switched_psi,"B")
    p_phi_b=event_probability(switched_phi,"B")
    error=max(*(abs(a[key]-b[key]) for key in a),
              abs(p_psi_a-p_psi_b),abs(p_phi_a-p_phi_b))
    if error>1e-10:raise AssertionError("frame covariance of geometry failed")
    # Classical total variation for a fixed binary relational measurement.
    tv=abs(p_psi_a-p_phi_a)
    if tv>a["trace_distance"]+1e-10:
        raise AssertionError("data-processing inequality failed")
    return {
        "protocol":"M45-ST67-RELATIONAL-QUANTUM-INFORMATION-GEOMETRY-v1",
        "a_frame_geometry":a,
        "b_frame_geometry":b,
        "relational_b_equals_c_probabilities":{"first":p_psi_a,"second":p_phi_a},
        "binary_measurement_total_variation":tv,
        "trace_distance_bounds_measurement_tv":tv<=a["trace_distance"]+1e-10,
        "max_frame_invariant_error":error,
        "interpretation":"PURE_STATE_UNITARY_GEOMETRY_INVARIANCE_NOT_NEW_PHYSICAL_METRIC"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--first",nargs=4,default=["1","0","1","0"])
    ap.add_argument("--second",nargs=4,default=["1","0","0","1"])
    args=ap.parse_args()
    print(json.dumps(analyze(args.first,args.second),indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
