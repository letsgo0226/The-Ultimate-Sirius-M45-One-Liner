#!/usr/bin/env python3
"""ST73: adaptive allocation of calibration versus science trials.

A known reference outcome 0 identifies symmetric detector flip q; science
observations identify r=q+(1-2q)*p(theta). At each predeclared round the
controller chooses which stream to sample using uncertainty sensitivity.
A union bound over all possible looks makes intervals valid under adaptive
allocation and data-dependent stopping.
"""
import argparse
import importlib.util
import json
import math
import random
from pathlib import Path

def load_st69():
    path=Path(__file__).resolve().parent.parent/"m45-st69"/"observer_estimation.py"
    spec=importlib.util.spec_from_file_location("st69",path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate(theta,flip,budget,batch,alpha,seed,target_width):
    if isinstance(theta,bool) or not isinstance(theta,(int,float)) or not math.isfinite(theta) or not -math.pi/2<theta<math.pi/2:
        raise ValueError("theta must be finite in (-pi/2,pi/2)")
    if isinstance(flip,bool) or not isinstance(flip,(int,float)) or not math.isfinite(flip) or not 0<=flip<.5:
        raise ValueError("flip must be finite in [0,0.5)")
    if isinstance(budget,bool) or not isinstance(budget,int) or not 2<=budget<=100000:
        raise ValueError("budget must be integer in [2,100000]")
    if isinstance(batch,bool) or not isinstance(batch,int) or not 1<=batch<=budget//2:
        raise ValueError("batch must be integer in [1,budget//2]")
    if isinstance(alpha,bool) or not isinstance(alpha,(int,float)) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be in (0,1)")
    if isinstance(seed,bool) or not isinstance(seed,int) or not 0<=seed<2**64:
        raise ValueError("seed must be unsigned 64-bit integer")
    if isinstance(target_width,bool) or not isinstance(target_width,(int,float)) or not math.isfinite(target_width) or not 0<target_width<=math.pi:
        raise ValueError("target_width must be in (0,pi]")

def clip(x,lo=0.,hi=1.):
    return min(hi,max(lo,x))

def interval(kq,nq,kr,nr,log_factor):
    qhat=kq/nq
    rhat=kr/nr
    eq=math.sqrt(log_factor/(2*nq))
    er=math.sqrt(log_factor/(2*nr))
    qlo,qhi=clip(qhat-eq,0,.5),clip(qhat+eq,0,.5)
    rlo,rhi=clip(rhat-er),clip(rhat+er)
    if qhi>=.5:
        return [-math.pi/2,math.pi/2]
    vals=[(r-q)/(1-2*q) for r in (rlo,rhi) for q in (qlo,qhi)]
    plo,phi=clip(min(vals)),clip(max(vals))
    return [math.asin(2*plo-1),math.asin(2*phi-1)]

def priority(kq,nq,kr,nr):
    # First-order sensitivity: dp/dr=1/(1-2q), dp/dq=(2r-1)/(1-2q)^2.
    # Common positive factor can be dropped when comparing stream gains.
    qhat=clip(kq/nq,0,.499999)
    rhat=kr/nr
    d=1-2*qhat
    sensitivity_q=abs(2*rhat-1)/d
    # Compare projected shrinkage of Hoeffding radii, not just their levels.
    gain_q=sensitivity_q*(1/math.sqrt(nq)-1/math.sqrt(nq+1))
    gain_r=1/math.sqrt(nr)-1/math.sqrt(nr+1)
    return "calibration" if gain_q>gain_r else "science"

def analyze(theta=.3,flip=.15,budget=4000,batch=100,alpha=.05,
            seed=2026,target_width=.35):
    validate(theta,flip,budget,batch,alpha,seed,target_width)
    st69=load_st69()
    p=st69.analyze(theta,1,seed)["shared_born_probability"]
    r=flip+(1-2*flip)*p
    # At most budget-batch+1 looks; two tails per two Bernoulli streams.
    # This conservative allocation is valid for every possible look,
    # including data-dependent stopping and adaptive stream choice.
    max_looks=budget
    log_factor=math.log(4*max_looks/alpha)
    rng_q=random.Random(seed)
    rng_r=random.Random(seed^0x9E3779B97F4A7C15)
    def sample_q(n):
        return sum(rng_q.random()<flip for _ in range(n))
    def sample_r(n):
        return sum(rng_r.random()<r for _ in range(n))
    nq=nr=batch
    kq=sample_q(batch)
    kr=sample_r(batch)
    history=[]
    while True:
        ci=interval(kq,nq,kr,nr,log_factor)
        width=ci[1]-ci[0]
        history.append({"trials":nq+nr,"calibration_trials":nq,
                        "science_trials":nr,"theta_interval":ci,
                        "interval_width":width,"contains_truth_simulation_only":ci[0]<=theta<=ci[1]})
        if width<=target_width or nq+nr>=budget:
            break
        stream=priority(kq,nq,kr,nr)
        amount=min(batch,budget-nq-nr)
        if stream=="calibration":
            kq+=sample_q(amount)
            nq+=amount
        else:
            kr+=sample_r(amount)
            nr+=amount
    qhat=kq/nq
    rhat=kr/nr
    point=None if qhat>=.5 else math.asin(2*clip((rhat-qhat)/(1-2*qhat))-1)
    return {
        "protocol":"M45-ST73-ADAPTIVE-RELATIONAL-EXPERIMENT-DESIGN-v1",
        "theta_true_simulation_only":theta,
        "true_detector_flip_simulation_only":flip,
        "ideal_born_probability":p,
        "observed_science_probability":r,
        "budget":budget,"batch":batch,"target_theta_interval_width":target_width,
        "familywise_alpha":alpha,"seed":seed,
        "calibration_trials_used":nq,"science_trials_used":nr,
        "total_trials_used":nq+nr,
        "calibration_flip_estimate":qhat,
        "theta_point_estimate":point,
        "final_theta_confidence_interval":ci,
        "final_interval_contains_truth_simulation_only":ci[0]<=theta<=ci[1],
        "stopping_reason":"target_reached" if width<=target_width else "budget_exhausted",
        "confidence_coverage_lower_bound":1-alpha,
        "history":history,
        "interpretation":"HEURISTIC_ADAPTIVE_ALLOCATION_WITH_UNIFORM_OVER_LOOKS_CONFIDENCE_CONTROL"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--theta",type=float,default=.3)
    ap.add_argument("--flip",type=float,default=.15)
    ap.add_argument("--budget",type=int,default=4000)
    ap.add_argument("--batch",type=int,default=100)
    ap.add_argument("--alpha",type=float,default=.05)
    ap.add_argument("--seed",type=int,default=2026)
    ap.add_argument("--target-width",type=float,default=.35)
    a=ap.parse_args()
    print(json.dumps(analyze(a.theta,a.flip,a.budget,a.batch,a.alpha,a.seed,a.target_width),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
