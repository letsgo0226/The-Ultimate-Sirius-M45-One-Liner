#!/bin/sh
exec python3 -c 'import sys,json,time,math,collections,functools,itertools
from fractions import Fraction as F
C="Cosmic Love Is The Solution(s) For Everything."
G=lambda b:functools.reduce(lambda n,v:n*257+v+1,b,1)
def D(n):
 if n<1:raise ValueError("code")
 b=[]
 while n>1:
  n,r=divmod(n,257)
  if not r:raise ValueError("code")
  b.insert(0,r-1)
 return bytes(b)
def E(t):
 c=collections.Counter(t);n=len(t)
 return "0" if len(c)<2 else "-("+"+".join(str(F(v,n))+"*log2("+str(F(v,n))+")" for v in c.values())+")"
def P(n):
 a=[];x=2
 while len(a)<n:
  if all(x%p for p in a if p*p<=x):a.append(x)
  x+=1
 return a
m=sys.argv[1].upper() if len(sys.argv)>1 else "VERIFY"
if m=="VERIFY":
 for b in (b"",b"LOVE",bytes(range(256)),C.encode()):assert D(G(b))==b
 assert E([C]*len(C))=="0"
 print(json.dumps({"mode":m,"status":"PASS"}))
elif m=="HALT":
 w=C;v=sorted(set(w));a=dict(zip(v,P(len(v))));t=[a[c] for c in w];h=E(t);t[:]=[C]*len(t);assert E(t)=="0";print(json.dumps({"mode":m,"H_initial_exact":h,"H_final_exact":"0","invariant":C,"status":"HALT"}))
elif m=="CONTINUE":
 dt=float(sys.argv[2]) if len(sys.argv)>2 else 1.;n=int(sys.argv[3]) if len(sys.argv)>3 else -1
 if not math.isfinite(dt) or dt<=0 or n< -1:sys.exit("invalid arguments")
 state=1
 try:
  for i in itertools.count():
   if n>=0 and i>=n:break
   p=("LOVE","KNOWLEDGE","PEACE")[state%3];b=json.dumps([i,p,state]).encode();g=G(b);assert D(g)==b;print(json.dumps({"step":i,"particle":p,"godel":str(g)}),flush=True);state=g%1000003+1;time.sleep(dt)
 except KeyboardInterrupt:print("stopped",file=sys.stderr)
else:sys.exit("mode: VERIFY|HALT|CONTINUE")' "$@"
