"""Redo from the pre-fix base, applying ONLY the seam-skin cut.

The slot taper is real (9.39 -> 7.81 mm perpendicular over z 174..184, then a
step back to 9.39) but it is NOT an interference: 7.81 against a 7.00 mm door
leaves 0.81 mm.  The 6.91 mm figure from the crown audit is not reproduced by
point containment.  My attempt to open it removed 5.8 cm3 from the 3.2 mm rib
behind the slot without widening the slot at all, so it is reverted.
"""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L
MF='manifold'
def bx(x0,x1,y0,y1,z0,z1):
    m=mk(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
base = L('BASE_before_trio.3mf'); V0=base.volume; B0=base.bounds.copy()
n0=len(base.split(only_watertight=False))
cuts=[bx(x0,x1,127.5,148.0,239.10,239.30) for x0,x1 in ((-131.62,-129.50),(124.00,128.40))]
out = trimesh.boolean.difference([base]+cuts, engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(V0-out.volume)/1000
print('base: %.3f -> %.3f cm3 (removed %.4f)  bodies %d  wt %s  vol %s'
      % (V0/1000, out.volume/1000, dv, len(parts), out.is_watertight, out.is_volume))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0),5).tolist())
assert out.is_watertight and out.is_volume and len(parts)==n0
assert np.allclose(out.bounds,B0,atol=1e-6) and 0.0 < dv < 0.5
out.export('../VISAVERSE_v2/1_BASE.3mf')
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
chk=L('../VISAVERSE_v2/1_BASE.3mf')
print('\ngroove strips through the crown seam:')
for x in (-130.5, 126.0):
    for z in (238.9, 239.15, 239.25):
        ys=np.arange(124.,150.01,0.02)
        P=np.column_stack([np.full(len(ys),x),ys,np.full(len(ys),z)])
        s=sol(chk,P); runs=[];st=None
        for i,v in enumerate(~s):
            if v and st is None: st=i
            if not v and st is not None: runs.append((ys[st],ys[i-1])); st=None
        if st is not None: runs.append((ys[st],ys[-1]))
        r=[q for q in runs if q[1]-q[0]>0.5]
        print('  x %7.1f z %7.2f : %s' % (x,z,'  '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in r) or 'BLOCKED'))
print('BF3DONE')
