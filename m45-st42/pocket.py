#!/usr/bin/env python3
"""ST42: exact finite prime Gödel coding, universal integer projection, pocket retrieval.

All "consciousness" and Doraemon terminology is fictional metadata, not mind transfer.
"""
import argparse
import hashlib
import json
from pathlib import Path

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def digest(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

def first_primes(k):
    if type(k) is not int or not 1<=k<=16:raise ValueError("k must be 1..16")
    out=[]
    c=2
    while len(out)<k:
        if all(c%p for p in out if p*p<=c):out.append(c)
        c+=1
    return out

def encode(values):
    if not isinstance(values,list) or not 1<=len(values)<=16 or any(
        type(v) is not int or not 0<=v<=64 for v in values):
        raise ValueError("expected 1..16 nonnegative integers <=64")
    n=1
    for p,v in zip(first_primes(len(values)),values):
        n*=pow(p,v+1)
    return n

def valuation(n,p):
    if type(n) is not int or n<1:raise ValueError("positive integer required")
    count=0
    while n%p==0:
        n//=p
        count+=1
    return count

def project(n,k):
    """Defined on all positive integers; generally many-to-one."""
    return [valuation(n,p) for p in first_primes(k)]

def decode(n,k):
    """Inverse of encode on its exact image; rejects noncanonical integers."""
    if type(n) is not int or n<1:raise ValueError("positive integer required")
    exponents=project(n,k)
    if any(e<1 or e>65 for e in exponents):
        raise ValueError("not a valid encoded state")
    values=[e-1 for e in exponents]
    if encode(values)!=n:raise ValueError("extra prime factors or noncanonical code")
    return values

def pocket_record(name,values,message):
    if not isinstance(name,str) or not 1<=len(name)<=80:
        raise ValueError("invalid name")
    if not isinstance(message,str) or len(message)>1000:
        raise ValueError("invalid text")
    n=encode(values)
    body={"protocol":"M45-ST42-POCKET-v1","name":name,"values":values,
          "godel_number":str(n),"message":message,
          "meaning":"FICTIONAL_CHARACTER_MEMORY_NOT_CONSCIOUSNESS"}
    return {**body,"sha256":digest(body)}

def verify(record):
    if not isinstance(record,dict):return False
    try:
        body=dict(record)
        claimed=body.pop("sha256")
        if digest(body)!=claimed:return False
        expected=pocket_record(body["name"],body["values"],body["message"])
        return expected==record and decode(int(body["godel_number"]),len(body["values"]))==body["values"]
    except (KeyError,ValueError,TypeError,OverflowError):
        return False

def retrieve(records,code):
    """Exact code match, not a claim of semantic mind-reading."""
    if type(code) is not int or code<1:raise ValueError("positive code required")
    if not isinstance(records,list) or any(not verify(r) for r in records):
        raise ValueError("invalid pocket records")
    return [r for r in records if int(r["godel_number"])==code]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--values",default="1,0,2")
    p.add_argument("--name",default="Doraemon fictional memory")
    p.add_argument("--message",default="Help others without forgetting their freedom.")
    p.add_argument("--out",default="m45-st42-pocket.json")
    a=p.parse_args()
    values=[int(x) for x in a.values.split(",")]
    record=pocket_record(a.name,values,a.message)
    assert verify(record)
    Path(a.out).write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(canonical({"verified":True,"godel_number":record["godel_number"],
                     "decoded":decode(int(record["godel_number"]),len(values)),
                     "retrieved":len(retrieve([record],int(record["godel_number"])))}))
if __name__=="__main__":main()
