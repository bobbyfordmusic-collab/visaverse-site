"""Redo from the pre-cut base.  The membrane is ONLY the 0.22 mm patch at
y 107..117, z 31..43 (elsewhere in that band the wall is a solid 0.70-1.12 mm
and must not be touched)."""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L
MF='manifold'
base=L('BASE_before_skin.3mf'); V0=base.volume; B0=base.bounds.copy()
n0=len(base.split(only_watertight=False))
cut = mk(extents=[0.36, 11.0, 13.0])
cut.apply_translation([-132.08, 112.0, 37.0])       # x -132.26..-131.90
out = trimesh.boolean.difference([base,cut], engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(V0-out.volume)/1000
print('base: %.3f -> %.3f cm3 (removed %.4f)  bodies %d -> %d  wt %s  vol %s'
      % (V0/1000,out.volume/1000,dv,n0,len(parts),out.is_watertight,out.is_volume))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0),5).tolist())
assert out.is_watertight and out.is_volume and len(parts)==n0
assert np.allclose(out.bounds,B0,atol=1e-6) and dv < 0.05
out.export('../VISAVERSE_v2/1_BASE.3mf')
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
chk=L('../VISAVERSE_v2/1_BASE.3mf')
print('\nverify - material in x -132.6..-131.5:')
for y in (100.,106.,110.,114.,118.,122.):
    row=[]
    for z in (26.,32.,38.,42.,48.):
        xs=np.arange(-132.6,-131.49,0.02)
        P=np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
        row.append('%.2f'%(sol(chk,P).sum()*0.02))
    print('  y %5.1f z26/32/38/42/48 : %s' % (y,'  '.join(row)))
print('SK2DONE')
