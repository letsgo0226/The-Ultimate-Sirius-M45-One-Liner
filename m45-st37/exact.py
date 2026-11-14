#!/usr/bin/env python3
"""M45-ST37 exact SK trace verifier with an independently implemented reducer.

Exact here means symbolic equality under the specified SK reduction strategy,
not a proof of universal software/hardware correctness.
"""
import argparse
import hashlib
import json
from pathlib import Path
import importlib.util

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("st32",BASE/"m45-st32"/"sk_tape.py")
producer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)

def parse(text):
    if not isinstance(text,str) or not 1<=len(text)<=300 or any(c not in "@SK" for c in text):
        raise ValueError("invalid SK expression")
    def walk(i,depth):
        if i>=len(text) or depth>300:raise ValueError("malformed SK expression")
        if text[i] in "SK":return text[i],i+1
        left,j=walk(i+1,depth+1)
        right,k=walk(j,depth+1)
        return [left,right],k
    tree,end=walk(0,0)
    if end!=len(text):raise ValueError("trailing symbols")
    return tree

def render(t):
    return t if isinstance(t,str) else "@"+render(t[0])+render(t[1])

def one_step(t):
    # Independent pattern-based leftmost-outermost SK reducer.
    if isinstance(t,str):return None
    if isinstance(t[0],list) and t[0][0]=="K":
        return t[0][1]
    if isinstance(t[0],list) and isinstance(t[0][0],list) and t[0][0][0]=="S":
        x=t[0][0][1]
        y=t[0][1]
        z=t[1]
        return [[x,z],[y,z]]
    left=one_step(t[0])
    if left is not None:return [left,t[1]]
    right=one_step(t[1])
    if right is not None:return [t[0],right]
    return None

def check_step(before,after):
    nxt=one_step(parse(before))
    return nxt is not None and render(nxt)==after

def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def certify(expression,budget=30,cap=10000):
    if type(budget) is not int or not 0<=budget<=100:
        raise ValueError("budget out of range")
    if type(cap) is not int or not 1<=cap<=300:
        raise ValueError("cap out of range")
    tree=producer.parse(expression)
    current=producer.encode(tree)
    trace=[]
    status="PAUSED"
    if len(current)>cap:
        status="CAP_EXCEEDED"
    else:
        for _ in range(budget):
            nxt=producer.reduce_once(tree)
            if nxt is None:
                status="NORMAL"
                break
            after=producer.encode(nxt)
            if len(after)>cap:
                status="CAP_EXCEEDED"
                break
            trace.append({"before":current,"after":after})
            current,tree=after,nxt
        else:
            if producer.reduce_once(tree) is None:status="NORMAL"
    result={"protocol":"M45-ST37","expression":expression,"budget":budget,"cap":cap,
            "trace":trace,"result":current,"status":status,"steps":len(trace)}
    result["sha256"]=sha(result)
    if not verify(result):raise AssertionError("independent verification failed")
    return result

def verify(cert):
    if not isinstance(cert,dict):return False
    try:
        content=dict(cert)
        claimed=content.pop("sha256")
        if sha(content)!=claimed:return False
        expr=content["expression"]
        parse(expr)
        budget,cap=content["budget"],content["cap"]
        if type(budget) is not int or not 0<=budget<=100 or type(cap) is not int or not 1<=cap<=300:
            return False
        trace=content["trace"]
        if not isinstance(trace,list) or len(trace)>budget:return False
        current=expr
        if len(current)>cap:
            return content["status"]=="CAP_EXCEEDED" and not trace and content["result"]==expr and content["steps"]==0
        for step in trace:
            if step["before"]!=current or len(step["after"])>cap or not check_step(current,step["after"]):
                return False
            current=step["after"]
        if current!=content["result"] or content["steps"]!=len(trace):return False
        nxt=one_step(parse(current))
        if content["status"]=="NORMAL":return nxt is None
        if content["status"]=="PAUSED":return nxt is not None and len(trace)==budget
        if content["status"]=="CAP_EXCEEDED":
            return nxt is not None and len(render(nxt))>cap
        return False
    except (KeyError,ValueError,TypeError,RecursionError,IndexError,AttributeError):
        return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--expression",default="@@@SKKS")
    p.add_argument("--budget",type=int,default=30)
    p.add_argument("--cap",type=int,default=300)
    p.add_argument("--out",default="m45-st37-certificate.json")
    a=p.parse_args()
    cert=certify(a.expression,a.budget,a.cap)
    Path(a.out).write_text(json.dumps(cert,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":cert["status"],"result":cert["result"],"steps":cert["steps"],"verified":verify(cert)}))

if __name__=="__main__":main()
