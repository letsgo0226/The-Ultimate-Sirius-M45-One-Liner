#!/usr/bin/env python3
"""ST72: independent reference-calibration and corrected relational inference.

Each observer calibrates a symmetric binary-flip detector using a known
reference outcome 0, then measures the ST69 relational event. Simultaneous
Hoeffding intervals propagate both calibration and science-sample uncertainty.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load_st69():
    path=Path(__file__).resolve().parent.parent/"m45-st69"/"observer_estimation.py"
    spec=importlib.util.spec_from_file_location("st69_estimation",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,actual,assumed,calibration_shots,science_shots,alpha,seed):
    if isinstance(theta,bool) or not isinstance(theta,(int,float)) or not math.isfinite(theta) or not -math.pi/2<theta<math.pi/2:
        raise ValueError("theta must be finite in (-pi/2,pi/2)")
    if len(actual)!=len(assumed) or not 2<=len(actual)<=100:
        raise ValueError("actual/assumed detector arrays must have equal length 2..100")
    if any(isinstance(q,bool) or not isinstance(q,(int,float)) or not math.isfinite(q) or not 0<=q<.5 for q in list(actual)+list(assumed)):
        raise ValueError("all detector flip rates must be finite in [0,0.5)")
    if any(isinstance(n,bool) or not isinstance(n,int) or not 1<=n<=100000 for n in (calibration_shots,science_shots)):
        raise ValueError("shots must be integer in [1,100000]")
    if len(actual)*(calibration_shots+science_shots)>1000000:
        raise ValueError("total simulated trials must not exceed 1e6")
    if isinstance(alpha,bool) or not isinstance(alpha,(int,float)) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be in (0,1)")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")

def clip(x,lo=0.,hi=1.):
    return min(hi,max(lo,x))

def theta_of_p(p):
    return math.asin(2*clip(p)-1)

def inverted_probability_interval(r_interval,q_interval):
    """Sharp corner bounds for p=(r-q)/(1-2q), q<1/2.

    If calibration uncertainty reaches q=1/2, the inversion is unidentifiable
    and the conservative p interval is [0,1].
    """
    qlo,qhi=q_interval
    rlo,rhi=r_interval
    if qhi>=.5:
        return [0.,1.]
    values=[(r-q)/(1-2*q) for r in (rlo,rhi) for q in (qlo,qhi)]
    return [clip(min(values)),clip(max(values))]

def analyze(theta=.3,actual=(.02,.08,.15,.04),
            assumed=(.02,.08,.02,.04),calibration_shots=2000,
            science_shots=2000,alpha=.05,seed=2026):
    actual=list(actual)
    assumed=list(assumed)
    validate(theta,actual,assumed,calibration_shots,science_shots,alpha,seed)
    st69=load_st69()
    p=st69.analyze(theta,1,seed)["shared_born_probability"]
    m=len(actual)
    # 2m individual Hoeffding events (calibration and science for each observer).
    # Each gets alpha/(2m): 2 exp(-2n eps^2)=alpha/(2m).
    log_factor=math.log(4*m/alpha)
    eps_q=math.sqrt(log_factor/(2*calibration_shots))
    eps_r=math.sqrt(log_factor/(2*science_shots))
    reports=[]
    calibrated_intervals=[]
    assumed_intervals=[]
    for i,(true_q,old_q) in enumerate(zip(actual,assumed)):
        rng_cal=random.Random((seed+2*i*0x9E3779B97F4A7C15)%(2**64))
        rng_science=random.Random((seed+(2*i+1)*0x9E3779B97F4A7C15)%(2**64))
        # Known reference outcome 0: observed '1' rate equals flip probability q.
        calibration_errors=sum(rng_cal.random()<true_q for _ in range(calibration_shots))
        measured_successes=sum(rng_science.random()<(true_q+(1-2*true_q)*p)
                               for _ in range(science_shots))
        qhat=calibration_errors/calibration_shots
        rhat=measured_successes/science_shots
        q_interval=[clip(qhat-eps_q,0.,.5),clip(qhat+eps_q,0.,.5)]
        r_interval=[clip(rhat-eps_r),clip(rhat+eps_r)]
        calibrated_p_interval=inverted_probability_interval(r_interval,q_interval)
        calibrated_theta_interval=[theta_of_p(x) for x in calibrated_p_interval]
        calibrated_intervals.append(calibrated_theta_interval)
        corrected_point=None if qhat>=.5 else theta_of_p((rhat-qhat)/(1-2*qhat))
        old_interval=[theta_of_p(x) for x in inverted_probability_interval(r_interval,[old_q,old_q])]
        assumed_intervals.append(old_interval)
        reports.append({
            "observer":i+1,"true_flip_rate_simulation_only":true_q,
            "previous_assumed_flip_rate":old_q,
            "calibration_errors":calibration_errors,
            "calibration_shots":calibration_shots,
            "estimated_flip_rate":qhat,
            "flip_rate_confidence_interval":q_interval,
            "science_successes":measured_successes,
            "science_shots":science_shots,
            "calibrated_theta_point_estimate":corrected_point,
            "calibrated_theta_confidence_interval":calibrated_theta_interval,
            "old_assumption_theta_interval":old_interval,
            "calibrated_interval_covers_truth":calibrated_theta_interval[0]<=theta<=calibrated_theta_interval[1]
        })
    def intersection(intervals):
        lo=max(x[0] for x in intervals)
        hi=min(x[1] for x in intervals)
        return [lo,hi] if lo<=hi else None
    return {
        "protocol":"M45-ST72-RELATIONAL-SELF-CALIBRATION-v1",
        "theta_true_simulation_only":theta,
        "shared_ideal_born_probability":p,
        "reference_known_binary_outcome":0,
        "familywise_alpha":alpha,
        "simultaneous_coverage_lower_bound":1-alpha,
        "calibration_hoeffding_radius":eps_q,
        "science_hoeffding_radius":eps_r,
        "observers":reports,
        "calibrated_consensus_interval":intersection(calibrated_intervals),
        "old_assumption_consensus_interval":intersection(assumed_intervals),
        "all_calibrated_intervals_cover_truth":all(x["calibrated_interval_covers_truth"] for x in reports),
        "interpretation":"REFERENCE_CALIBRATION_MAKES_DETECTOR_ERROR_IDENTIFIABLE; INTERVALS_PROPAGATE_CALIBRATION_UNCERTAINTY"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--actual-flips",default="0.02,0.08,0.15,0.04")
    ap.add_argument("--assumed-flips",default="0.02,0.08,0.02,0.04")
    ap.add_argument("--calibration-shots",type=int,default=2000)
    ap.add_argument("--science-shots",type=int,default=2000)
    ap.add_argument("--alpha",type=float,default=.05)
    ap.add_argument("--seed",type=int,default=2026)
    a=ap.parse_args()
    st71=Path(__file__).resolve().parent.parent/"m45-st71"/"model_disagreement.py"
    spec=importlib.util.spec_from_file_location("st71",st71)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print(json.dumps(analyze(a.theta,mod.parse_rates(a.actual_flips),
                             mod.parse_rates(a.assumed_flips),
                             a.calibration_shots,a.science_shots,a.alpha,a.seed),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
