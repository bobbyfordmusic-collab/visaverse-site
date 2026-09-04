import numpy as np, trimesh
def L(fn):
    m=trimesh.load(fn,process=False)
    return trimesh.util.concatenate(list(m.geometry.values())) if isinstance(m,trimesh.Scene) else m
def inside(mesh,P,chunk=3000):
    P=np.asarray(P,float); out=np.zeros(len(P),bool)
    for i in range(0,len(P),chunk):
        out[i:i+chunk]=mesh.contains(P[i:i+chunk])
    return out
def runs(mask,axis):
    out=[];s=None
    for i,x in enumerate(mask):
        if x and s is None: s=i
        if not x and s is not None: out.append((axis[s],axis[i-1])); s=None
    if s is not None: out.append((axis[s],axis[-1]))
    return out
from trimesh.creation import box as _mk
def crop(mesh,lo,hi):
    e=[hi[i]-lo[i] for i in range(3)]; c=[(lo[i]+hi[i])/2 for i in range(3)]
    t=_mk(extents=e); t.apply_translation(c)
    return trimesh.boolean.intersection([mesh,t],engine='manifold')
SLOPE_W=np.array([0.,-0.6425,0.7663]); SLOPE_W/=np.linalg.norm(SLOPE_W)
_U=np.array([1.,0,0]); _V=np.cross(SLOPE_W,_U)
R=np.column_stack([_U,_V,SLOPE_W])
Ts=np.eye(4); Ts[:3,:3]=R.T
Tb=np.eye(4); Tb[:3,:3]=R
