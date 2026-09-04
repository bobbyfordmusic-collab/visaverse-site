"""Measure the cavity-floor wedge, then close it with a single small union."""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L
MF='manifold'
base=L('../VISAVERSE_v2/1_BASE.3mf')
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def gap(m,x,y):
    zs=np.arange(41.0,45.0,0.005)
    P=np.column_stack([np.full(len(zs),x), np.full(len(zs),y), zs])
    s=~sol(m,P); runs=[];st=None
    for i,v in enumerate(s):
        if v and st is None: st=i
        if not v and st is not None: runs.append((zs[st],zs[i-1])); st=None
    if st is not None: runs.append((zs[st],zs[-1]))
    r=[q for q in runs if q[1]-q[0]>0.002]
    return r[0] if r else None
print('  x      y=99    y=101   y=103   y=105   y=106')
zlo=[];zhi=[];ys=[]
for x in (-100.,0.,110.):
    row=[]
    for y in (99.,101.,103.,105.,106.):
        g=gap(base,x,y)
        if g: row.append('%.3f'%(g[1]-g[0])); zlo.append(g[0]); zhi.append(g[1]); ys.append(y)
        else: row.append('  .   ')
    print('  %6.0f %s' % (x,'  '.join(row)))
if not ys:
    print('no wedge found'); print('W2DONE'); raise SystemExit
Z0,Z1 = min(zlo)-0.03, max(zhi)+0.03
Y0,Y1 = 97.0, min(max(ys), 105.4)
print('\nwedge z %.3f..%.3f ; filling x -122..122, y %.1f..%.1f' % (Z0,Z1,Y0,Y1))
V0=base.volume; B0=base.bounds.copy(); n0=len(base.split(only_watertight=False))
fill = mk(extents=[244.0, Y1-Y0, Z1-Z0])
fill.apply_translation([-1.9, (Y0+Y1)/2., (Z0+Z1)/2.])
out = trimesh.boolean.union([base, fill], engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(out.volume-V0)/1000
print('base: %.3f -> %.3f cm3 (added %.4f)  bodies %d -> %d  wt %s  vol %s'
      % (V0/1000,out.volume/1000,dv,n0,len(parts),out.is_watertight,out.is_volume))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0),5).tolist())
assert out.is_watertight and out.is_volume and len(parts)==n0
assert np.allclose(out.bounds,B0,atol=1e-6) and 0.0 <= dv < 1.5
out.export('../VISAVERSE_v2/1_BASE.3mf')
chk=L('../VISAVERSE_v2/1_BASE.3mf')
print('verify:', [(int(x),int(y), 'closed' if gap(chk,x,y) is None else 'STILL OPEN')
                  for x,y in ((-100.,101.),(0.,103.),(110.,101.))])
print('W2DONE')
