"""The pull's shank is a Ø4.980 x 3.4 peg then a Ø6.95 x 2.4 locating boss.
The door's socket is Ø6.880 - 0.07 mm too small for the boss, so the boss
cannot enter and the pull hangs on the peg with 1.90 mm of slop.  The near-miss
says the boss was meant to be the locating feature.

Open the sockets to Ø7.30, concentric with the peg/boss axes (door x -32.775 /
+27.225, y 0.825 - the existing sockets are 0.075 mm off that), keeping the
1.63 mm floor behind them.
"""
import trimesh, numpy as np
from _occ import L
MF='manifold'
D='../VISAVERSE_v2/'
lo = L(D+'4_SHUTTER_LOWER.3mf'); V0=lo.volume; B0=lo.bounds.copy()
n0=len(lo.split(only_watertight=False))
print('lower panel in: %.3f cm3, %d bodies, wt %s' % (V0/1000,n0,lo.is_watertight))
cuts=[]
for cx in (-32.775, 27.225):
    c = trimesh.creation.cylinder(radius=7.30/2., height=9.2, sections=96)
    c.apply_translation([cx, 0.825, -1.0+9.2/2.])      # z -1.0 .. 7.12
    cuts.append(c)
out = trimesh.boolean.difference([lo]+cuts, engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>0.5]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(V0-out.volume)/1000
print('lower panel out: %.3f cm3 (removed %.4f)  bodies %d  wt %s  vol %s'
      % (out.volume/1000,dv,len(parts),out.is_watertight,out.is_volume))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0),5).tolist())
assert out.is_watertight and out.is_volume
assert np.allclose(out.bounds,B0,atol=1e-6), 'outer bounds moved'
assert 0.0 < dv < 0.5, 'removed %.4f cm3' % dv
out.export(D+'4_SHUTTER_LOWER.3mf')
print('bodies %d -> %d (sacrificial pads are separate bodies, count may shift)' % (n0,len(parts)))

# ---- verify the pull now seats -------------------------------------------
chk = L(D+'4_SHUTTER_LOWER.3mf')
pull = L(D+'8_DOOR_PULL.3mf')
M=np.eye(4); M[:3,:3]=np.diag([1.,-1.,-1.]); M[:3,3]=[-2.775,0.825,3.60]
pull.apply_transform(M)
i = trimesh.boolean.intersection([pull, chk], engine=MF)
print('\npull ^ lower panel: %.5f cm3' % (0. if i.is_empty else abs(i.volume)/1000))
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i_ in range(0,len(P),2000): o[i_:i_+2000]=m.contains(P[i_:i_+2000])
    return o
def span(m,y,z,x0=-40.,x1=40.):
    xs=np.arange(x0,x1,0.01)
    P=np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
    s=~sol(m,P); runs=[];st=None
    for i_,v in enumerate(s):
        if v and st is None: st=i_
        if not v and st is not None: runs.append((xs[st],xs[i_-1])); st=None
    if st is not None: runs.append((xs[st],xs[-1]))
    return [r for r in runs if r[1]-r[0]>2.]
print('socket bore now:')
for z in (1.0, 3.0, 5.0, 6.8):
    print('   z %4.1f : %s' % (z,'  '.join('c=%.3f d=%.3f'%((a+b)/2,b-a) for a,b in span(chk,0.825,z))))
print('PSDONE')
