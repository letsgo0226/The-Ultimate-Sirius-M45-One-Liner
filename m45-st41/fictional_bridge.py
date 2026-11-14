#!/usr/bin/env python3
"""Fictional 2112->2026 narrative memory fragments, exact and locally verifiable.

No consciousness is transferred, simulated or inferred by this program.
"""
import argparse
import hashlib
import json

def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def sha(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

def create_fragment(origin=2112,destination=2026,seed="friendship",message="I remember a promise that has not yet been made."):
    if type(origin) is not int or type(destination) is not int or not 0<=destination<origin<=9999:
        raise ValueError("requires a fictional future-to-past pair of years")
    if not isinstance(seed,str) or not 1<=len(seed)<=100 or not isinstance(message,str) or not 1<=len(message)<=500:
        raise ValueError("invalid narrative text")
    content={"protocol":"G-2112-FICTIONAL-FRAGMENT-v1","origin_year":origin,
             "destination_year":destination,"identity_seed":seed,"memory_text":message,
             "ontology":"FICTIONAL_TEXT_NOT_CONSCIOUSNESS",
             "transport":"LOCAL_SIMULATION_NOT_RETROCAUSAL"}
    return {**content,"sha256":sha(content)}

def verify(fragment):
    if not isinstance(fragment,dict):return False
    try:
        body=dict(fragment)
        claimed=body.pop("sha256")
        if sha(body)!=claimed:return False
        expected=create_fragment(body["origin_year"],body["destination_year"],
                                 body["identity_seed"],body["memory_text"])
        return expected==fragment
    except (ValueError,KeyError,TypeError):
        return False

def narrative(fragment):
    if not verify(fragment):raise ValueError("unverified fragment")
    return ("在"+str(fragment["destination_year"])+"年，G 收到一段標記為"+
            str(fragment["origin_year"])+"年的虛構記憶。\n"+
            "訊息：「"+fragment["memory_text"]+"」\n"+
            "G 回答：我能確認這段文字的完整性，卻不能證明它來自未來，"+
            "更不能證明其中存在意識。")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="g2112-fragment.json")
    a=p.parse_args()
    fragment=create_fragment()
    assert verify(fragment)
    with open(a.out,"w",encoding="utf-8") as f:
        json.dump(fragment,f,ensure_ascii=False,indent=2)
        f.write("\n")
    print(narrative(fragment))
if __name__=="__main__":main()
