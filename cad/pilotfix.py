"""The sill cap seats at u = 0 - proved three ways: its x extents equal the
base's exactly, its magnets then line up with the door's to 0.00 mm, and its
right M3 hole lands dead on the base pilot at u +127.000.  Its left hole is at
u -130.000 but the base pilot is at -130.800, so the base's LEFT pilot is
0.800 mm out.  Fill it and re-drill at -130.000.
"""
import trimesh, numpy as np
from _occ import L, Ts, Tb
MF='manifold'
V_AX, W0, W1 = -68.20, 123.8, 137.6      # pilot axis position and w span
R_FILL, R_DRILL = 1.55, 1.32
def cyl(u, r, w0, w1):
    c = trimesh.creation.cylinder(radius=r, height=w1-w0, sections=64)
    T = np.eye(4); T[:3,3] = [u, V_AX, (w0+w1)/2.]
    c.apply_transform(T); c.apply_transform(Tb); return c
base = L('BASE_before_pilot.3mf'); V0=base.volume; B0=base.bounds.copy()
n0=len(base.split(only_watertight=False))
print('base in: %.3f cm3, %d bodies' % (V0/1000, n0))
work = trimesh.boolean.union([base, cyl(-130.800, R_FILL, W0, W1)], engine=MF)
print('after filling the old pilot: %.3f cm3 (+%.4f)' % (work.volume/1000,(work.volume-V0)/1000))
out  = trimesh.boolean.difference([work, cyl(-130.000, R_DRILL, W0+0.7, W1+0.4)], engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
print('after re-drilling      : %.3f cm3  net %+.4f  bodies %d  wt %s  vol %s'
      % (out.volume/1000,(out.volume-V0)/1000,len(parts),out.is_watertight,out.is_volume))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0),5).tolist())
assert out.is_watertight and out.is_volume and len(parts)==n0
assert np.allclose(out.bounds,B0,atol=1e-6)
out.export('../VISAVERSE_v2/1_BASE.3mf')
# verify
chk=L('../VISAVERSE_v2/1_BASE.3mf'); chk.apply_transform(Ts)
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
for w in (134.0, 136.0):
    us=np.arange(-136.,132.01,0.02)
    P=np.column_stack([us, np.full(len(us),V_AX), np.full(len(us),w)])
    s=~sol(chk,P); runs=[];st=None
    for i,v in enumerate(s):
        if v and st is None: st=i
        if not v and st is not None: runs.append((us[st],us[i-1])); st=None
    if st is not None: runs.append((us[st],us[-1]))
    r=[q for q in runs if 1.5<q[1]-q[0]<6.]
    print('  pilots at w %.1f : %s   (cap holes are -130.000 / +127.000)'
          % (w,'  '.join('c=%.3f d=%.2f'%((a+b)/2,b-a) for a,b in r)))
print('PFIXDONE')
