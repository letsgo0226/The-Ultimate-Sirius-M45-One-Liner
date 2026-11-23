# URFCO-06: bounded compatible direct limit
URFCO-05 CI 44922308302 passed.
Choose lambda_k=1/k for k>=1. On each pair use
M_k=[-1,lambda_k;0,1]. M_k^2=I, and every coordinate prefix
is invariant under the infinite block rule, including odd prefixes.
Zero padding therefore commutes with the action. On finitely
supported rational vectors this gives a well-defined involution.
On real or complex l2, write T=D+B, with D diagonal signs
and B mapping even coordinates into preceding odd coordinates.
||D||=1, ||B||<=1, hence ||T||<=2. The bounded extension
from the dense finite-support subspace is unique, and T^2=I
extends by continuity. This proof is mathematical, not machine
checked yet. New coordinates affect old ones within a pair;
old support cannot expand under T, as required by compatibility.
No inter-pair coupling, no claim of universal computation.
Tests enumerate 9840 ternary prefixes of lengths 1..8, check
two inverse applications, embedding and squared norm bound,
plus 32 nonzero couplings and invalid inputs. Exact Fraction;
finite implementation capped at 4096 coordinates. CI pending.
No merge, deployment, or modification of baseline Schumann Machine.
