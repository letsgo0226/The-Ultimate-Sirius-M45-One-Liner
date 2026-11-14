#!/usr/bin/env python3
"""ST48: bounded, read-only astronomical data acquisition from NASA/JPL Horizons.

An ephemeris is computed/model-derived data, not a new telescope observation.
"""
import argparse
import hashlib
import json
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

API="https://ssd.jpl.nasa.gov/api/horizons.api"
TARGETS={"sun":"10","moon":"301","mars":"499","jupiter":"599","venus":"299"}
MAX_RESPONSE=500000

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def request_url(target,day):
    if target not in TARGETS:raise ValueError("unsupported target")
    if not isinstance(day,str):raise ValueError("date must be string")
    d=date.fromisoformat(day)
    if not date(1900,1,1)<=d<=date(2100,12,30):raise ValueError("date out of bounds")
    params={"format":"json","COMMAND":f"'{TARGETS[target]}'",
            "OBJ_DATA":"'NO'","MAKE_EPHEM":"'YES'",
            "EPHEM_TYPE":"'OBSERVER'","CENTER":"'500@399'",
            "START_TIME":f"'{d.isoformat()}'",
            "STOP_TIME":f"'{(d+timedelta(days=1)).isoformat()}'",
            "STEP_SIZE":"'1 d'","QUANTITIES":"'1,9'"}
    return API+"?"+urllib.parse.urlencode(params)

def fetch(target,day,opener=None):
    url=request_url(target,day)
    if opener is None:opener=urllib.request.urlopen
    req=urllib.request.Request(url,headers={"User-Agent":"M45-ST48-Research-Prototype/1.0"})
    with opener(req,timeout=20) as response:
        raw=response.read(MAX_RESPONSE+1)
    if len(raw)>MAX_RESPONSE:raise ValueError("response exceeds limit")
    parsed=json.loads(raw.decode("utf-8"))
    if not isinstance(parsed,dict) or not isinstance(parsed.get("result"),str):
        raise ValueError("unexpected Horizons payload")
    result=parsed["result"]
    if "$$SOE" not in result or "$$EOE" not in result:
        raise ValueError("missing ephemeris table")
    if not isinstance(parsed.get("signature"),dict):
        raise ValueError("missing API signature")
    return make_record(target,day,url,parsed)

def make_record(target,day,url,payload):
    # Retain exact raw response, avoiding unreliable parsing of textual columns.
    body={"protocol":"M45-ST48-HORIZONS-v1","source":"NASA/JPL Horizons",
          "kind":"MODEL_EPHEMERIS_NOT_DIRECT_SENSOR_OBSERVATION",
          "target":target,"date_utc":day,"request_url":url,
          "api_signature":payload["signature"],"result":payload["result"]}
    return {**body,"sha256":hashlib.sha256(canonical(body).encode()).hexdigest()}

def verify(record):
    if not isinstance(record,dict):return False
    try:
        body=dict(record)
        claimed=body.pop("sha256")
        if set(body)!={"protocol","source","kind","target","date_utc","request_url","api_signature","result"}:
            return False
        if body["protocol"]!="M45-ST48-HORIZONS-v1" or body["source"]!="NASA/JPL Horizons":
            return False
        if body["kind"]!="MODEL_EPHEMERIS_NOT_DIRECT_SENSOR_OBSERVATION":
            return False
        if body["request_url"]!=request_url(body["target"],body["date_utc"]):
            return False
        if not isinstance(body["api_signature"],dict) or not isinstance(body["result"],str):
            return False
        if "$$SOE" not in body["result"] or "$$EOE" not in body["result"]:
            return False
        return hashlib.sha256(canonical(body).encode()).hexdigest()==claimed
    except (TypeError,KeyError,ValueError,OverflowError):
        return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",choices=sorted(TARGETS),default="mars")
    p.add_argument("--date",required=True)
    p.add_argument("--out",default="m45-st48-horizons.json")
    args=p.parse_args()
    record=fetch(args.target,args.date)
    if not verify(record):raise SystemExit("verification failed")
    Path(args.out).write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(canonical({"verified":True,"target":args.target,"date":args.date,
                     "sha256":record["sha256"],"kind":record["kind"]}))
if __name__=="__main__":main()
