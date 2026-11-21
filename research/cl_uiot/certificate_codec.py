"""Canonical full restricted certificate encoding, bounded and lossless."""
import json
from fractions import Fraction as Q
from correspondence import verify

LIMIT=4096

def pack(v):
    if type(v) is Q:
        return {"q":[v.numerator,v.denominator]}
    if type(v) is tuple:
        return [pack(x) for x in v]
    if type(v) is dict:
        return {k:pack(x) for k,x in v.items()}
    if type(v) in (int,str):
        return v
    raise ValueError("unsupported type")

def unpack(v):
    if type(v) is list:
        return tuple(map(unpack,v))
    if type(v) is dict:
        if set(v)=={"q"}:
            n,d=v["q"]
            if type(n) is not int or type(d) is not int or d<=0:
                raise ValueError("invalid fraction")
            return Q(n,d)
        return {k:unpack(x) for k,x in v.items()}
    if type(v) in (int,str):
        return v
    raise ValueError("unsupported type")

def serialize(record):
    if not verify(record):
        raise ValueError("invalid certificate")
    b=json.dumps(pack(record),sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
    if len(b)>LIMIT:
        raise ValueError("certificate limit")
    return b

def G(b):
    if type(b) is not bytes or len(b)>LIMIT:
        raise ValueError("byte limit")
    n=1
    for v in b:
        n=257*n+v+1
    return n

def D(n):
    if type(n) is not int or n<1 or n.bit_length()>9*(LIMIT+1):
        raise ValueError("code limit")
    out=bytearray()
    while n>1:
        n,r=divmod(n,257)
        if r==0 or len(out)>=LIMIT:
            raise ValueError("invalid digit or length")
        out.append(r-1)
    if n!=1:
        raise ValueError("invalid sentinel")
    return bytes(reversed(out))

def encode(record):
    return G(serialize(record))

def decode(n):
    b=D(n)
    try:
        r=unpack(json.loads(b.decode("ascii")))
        if serialize(r)!=b:
            raise ValueError("noncanonical certificate")
        return r
    except (TypeError,KeyError,ZeroDivisionError,RecursionError,OverflowError) as e:
        raise ValueError("invalid certificate") from e
