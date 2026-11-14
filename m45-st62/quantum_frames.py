#!/usr/bin/env python3
"""ST62: full complex qubit states and passive SU(2) frame covariance.

Uses the Bloch sphere, a general axis-angle SU(2) matrix, and simultaneous
transformation of state and measurement projector. No external dependencies.
"""
import argparse
import json
import math

I=((1+0j,0j),(0j,1+0j))
X=((0j,1+0j),(1+0j,0j))
Y=((0j,-1j),(1j,0j))
Z=((1+0j,0j),(0j,-1+0j))

def mul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))
def dagger(a):
    return tuple(tuple(a[j][i].conjugate() for j in range(2)) for i in range(2))
def trace(a):
    return a[0][0]+a[1][1]
def linear(terms):
    return tuple(tuple(sum(c*a[i][j] for c,a in terms) for j in range(2))
                 for i in range(2))
def norm3(v):
    return math.sqrt(sum(t*t for t in v))
def vec3(v,name,unit=False):
    if len(v)!=3 or any(isinstance(t,bool) or not isinstance(t,(float,int)) or not math.isfinite(t) for t in v):
        raise ValueError(name+" must contain three finite numbers")
    v=tuple(float(t) for t in v)
    r=norm3(v)
    if unit and r==0:raise ValueError(name+" must be nonzero")
    if unit:return tuple(t/r for t in v)
    if r>1+1e-12:raise ValueError(name+" outside Bloch ball")
    return v
def dot_pauli(v):
    return linear(tuple((v[i],p) for i,p in enumerate((X,Y,Z))))
def density(bloch):
    v=vec3(bloch,"bloch")
    return linear(((0.5,I),(0.5,dot_pauli(v))))
def projector(axis):
    v=vec3(axis,"measurement axis",True)
    return linear(((0.5,I),(0.5,dot_pauli(v))))
def rotation(axis,angle):
    v=vec3(axis,"rotation axis",True)
    if isinstance(angle,bool) or not isinstance(angle,(int,float)) or not math.isfinite(angle) or abs(angle)>1e6:
        raise ValueError("angle must be finite and bounded")
    return linear(((math.cos(angle/2),I),(-1j*math.sin(angle/2),dot_pauli(v))))
def real(x):
    if abs(x.imag)>1e-10:raise AssertionError("expected real quantity")
    return x.real
def prob(rho,measurement):
    return real(trace(mul(rho,measurement)))
def analyze(bloch=(0.3,0.4,0.5),measurement_axis=(0,0,1),
            rotation_axis=(1,2,3),angle=1.0):
    rho=density(bloch)
    measurement=projector(measurement_axis)
    u=rotation(rotation_axis,angle)
    ud=dagger(u)
    rotated_rho=mul(mul(u,rho),ud)
    rotated_measurement=mul(mul(u,measurement),ud)
    p=prob(rho,measurement)
    q=prob(rotated_rho,rotated_measurement)
    purity=real(trace(mul(rho,rho)))
    rotated_purity=real(trace(mul(rotated_rho,rotated_rho)))
    determinant=real(rho[0][0]*rho[1][1]-rho[0][1]*rho[1][0])
    rotated_det=real(rotated_rho[0][0]*rotated_rho[1][1]-rotated_rho[0][1]*rotated_rho[1][0])
    err=max(abs(p-q),abs(purity-rotated_purity),abs(determinant-rotated_det),
            abs(trace(rho)-trace(rotated_rho)),abs(trace(mul(u,ud))-2))
    if err>1e-10:raise AssertionError("SU(2) covariance or unitarity check failed")
    encode=lambda matrix:[[[v.real,v.imag] for v in row] for row in matrix]
    return {
        "protocol":"M45-ST62-GENERALIZED-QUANTUM-REFERENCE-FRAMES-v1",
        "bloch_vector":list(vec3(bloch,"bloch")),
        "measurement_axis":list(vec3(measurement_axis,"measurement axis",True)),
        "rotation_axis":list(vec3(rotation_axis,"rotation axis",True)),
        "angle_radians":angle,
        "density_matrix_complex_pairs":encode(rho),
        "unitary_complex_pairs":encode(u),
        "rotated_density_matrix_complex_pairs":encode(rotated_rho),
        "born_plus_original":p,
        "born_plus_transported":q,
        "purity_original":purity,
        "purity_transported":rotated_purity,
        "determinant_original":determinant,
        "determinant_transported":rotated_det,
        "max_invariant_error":err,
        "interpretation":"PASSIVE_SU2_COVARIANCE_NOT_IDENTICAL_INDIVIDUAL_OUTCOMES_OR_RELATIVISTIC_REFERENCE_FRAMES"
    }
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bloch",nargs=3,type=float,default=(0.3,0.4,0.5))
    ap.add_argument("--measurement-axis",nargs=3,type=float,default=(0,0,1))
    ap.add_argument("--rotation-axis",nargs=3,type=float,default=(1,2,3))
    ap.add_argument("--angle",type=float,default=1)
    a=ap.parse_args()
    print(json.dumps(analyze(a.bloch,a.measurement_axis,a.rotation_axis,a.angle),
                     indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
