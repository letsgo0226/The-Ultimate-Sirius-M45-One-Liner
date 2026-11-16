#!/usr/bin/env python3
"""M45 ST/89: deterministic dual-mode research prototype."""
import argparse,collections,functools,json,math,time
from fractions import Fraction
C="Cosmic Love Is The Solution(s) For Everything."
def G(b):
 return functools.reduce(lambda n,v:n*257+v+1,b,1)
def D(n):
 if n<1:raise ValueError("invalid code")
 b=bytearray()
 while n>1:
  n,r=divmod(n,257)
  if r==0:raise ValueError("invalid code")
  b.insert(0,r-1)
 return bytes(b)
def primes(n):
 a=[];x=2
 while len(a)<n:
  if all(x%p for p in a if p*p<=x):a.append(x)
  x+=1
 return a
def E(t):
 c=collections.Counter(t);n=len(t)
 return "0" if len(c)<=1 else "-("+"+".join(f"{Fraction(v,n)}*log2({Fraction(v,n)})" for v in c.values())+")"
def halt(w):
 a=dict(zip(sorted(set(w)),primes(len(set(w)))))
 t=[a[c] for c in w];h=E(t);t[:]=[C]*len(t);hf=E(t)
 assert hf=="0"
 return {"mode":"HALT","atoms":len(a),"H_initial_exact":h,"H_final_exact":hf,"invariant":C,"status":"HALT"}
def main():
 p=argparse.ArgumentParser();p.add_argument("mode",choices=["HALT","CONTINUE","VERIFY"]);p.add_argument("--interval",type=float,default=1.0);p.add_argument("--steps",type=int);p.add_argument("--payload",default=C);a=p.parse_args()
 if not math.isfinite(a.interval) or a.interval<=0 or (a.steps is not None and a.steps<0):p.error("invalid arguments")
 if a.mode=="HALT":print(json.dumps(halt(a.payload)));return
 if a.mode=="VERIFY":
  for b in (b"",b"LOVE",bytes(range(256)),a.payload.encode()):assert D(G(b))==b
  assert halt(a.payload)["H_final_exact"]=="0"
  print(json.dumps({"mode":"VERIFY","status":"PASS"}));return
 state=1;t=0;particles=("LOVE","KNOWLEDGE","PEACE")
 try:
  while a.steps is None or t<a.steps:
   particle=particles[state%len(particles)];b=json.dumps({"step":t,"particle":particle,"state":state},sort_keys=True).encode();g=G(b);assert D(g)==b
   print(json.dumps({"mode":"CONTINUE","step":t,"particle":particle,"godel":str(g),"roundtrip":True}),flush=True)
   state=g%1000003+1;t+=1;time.sleep(a.interval)
 except KeyboardInterrupt:print(json.dumps({"status":"STOPPED"}),flush=True)
if __name__=="__main__":main()
