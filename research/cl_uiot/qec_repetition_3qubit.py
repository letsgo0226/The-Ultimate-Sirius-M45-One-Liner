"""Exact three-qubit repetition code for single bit flips."""
from fractions import Fraction as Q
from quantum_entropy_2level import density

MASKS=(0,1,2,4)
CODE=(0,7)

def kl_block(a,b):
    if a not in range(8) or b not in range(8):raise ValueError("invalid mask")
    return tuple(tuple(int(i==(j^a^b)) for j in CODE) for i in CODE)

def correctable(masks):
    return all((lambda M:M[0][1]==M[1][0]==0 and M[0][0]==M[1][1])(kl_block(a,b))
               for a in masks for b in masks)

def encode(a,b):
    R=density(a,b)
    return tuple(tuple(R[CODE.index(i)][CODE.index(j)] if i in CODE and j in CODE else 0
                       for j in range(8)) for i in range(8))

def flip(R,mask):
    if mask not in range(8):raise ValueError("invalid mask")
    return tuple(tuple(R[i^mask][j^mask] for j in range(8)) for i in range(8))

def decode(R):
    # Syndrome measurement and correction, followed by logical decoding.
    return tuple(tuple(sum(R[i^m][j^m] for m in MASKS) for j in CODE) for i in CODE)

def noisy(a,b,weights):
    w=tuple(map(Q,weights))
    if len(w)!=4 or min(w)<0 or sum(w)!=1:raise ValueError("invalid probabilities")
    R=encode(a,b)
    return tuple(tuple(sum(p*R[i^m][j^m] for p,m in zip(w,MASKS))
                       for j in range(8)) for i in range(8))
