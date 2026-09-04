import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L, Ts, Tb
MF='manifold'
def bx(x0,x1,y0,y1,z0,z1):
    m=mk(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
# the pads hang below the cap's underside: own w 27.687..29.937.  Cut only there.
cap = L('CAP_before_sliver.3mf'); V0=cap.volume; B0=cap.bounds.copy()
caps = cap.copy(); caps.apply_transform(Ts)
cut = bx(123.30, 127.0, -172., -151., 24.0, 29.90)
out = trimesh.boolean.difference([caps, cut], engine=MF)
out.apply_transform(Tb)
dv=(V0-out.volume)/1000
print('cap: %.4f -> %.4f cm3 (removed %.4f), bodies %d, wt %s, bounds moved %s'
      % (V0/1000, out.volume/1000, dv, len(out.split(only_watertight=False)),
         out.is_watertight, not np.allclose(out.bounds,B0,atol=1e-6)))
assert out.is_watertight and 0.0 < dv < 0.02, 'removed %.4f cm3' % dv
out.export('../VISAVERSE_v2/9_SILL_CAP.3mf')
chk = L('../VISAVERSE_v2/9_SILL_CAP.3mf'); chk.apply_transform(Ts)
chk.apply_translation([-0.453, 93.063, 139.45-29.937])
for w in (137.6, 138.2, 138.8):
    us=np.arange(-140.,132.01,0.05)
    P=np.column_stack([us, np.full(len(us),-69.0), np.full(len(us),w)])
    m=sol(chk,P); runs=[];s=None
    for i,v in enumerate(m):
        if v and s is None: s=i
        if not v and s is not None: runs.append((us[s],us[i-1])); s=None
    if s is not None: runs.append((us[s],us[-1]))
    print('   pads at w %.1f: %s' % (w, '  '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in runs) or 'none'))

base = L('BASE_before_trio.3mf')
print('\nstow-slot perpendicular thickness through the reported pinch (door is 7.00)')
for x in (-100., 0., 100.):
    row=[]
    for z in np.arange(174., 192.1, 1.5):
        ys=np.arange(120.,165.01,0.01)
        P=np.column_stack([np.full(len(ys),x), ys, np.full(len(ys),z)])
        m=sol(base,P); runs=[];s=None
        for i,v in enumerate(~m):
            if v and s is None: s=i
            if not v and s is not None: runs.append((ys[s],ys[i-1])); s=None
        if s is not None: runs.append((ys[s],ys[-1]))
        r=[q for q in runs if 5.<q[1]-q[0]<15.]
        row.append((z,(r[0][1]-r[0][0])*0.9848 if r else 0.))
    print('  x %6.0f : %s' % (x,'  '.join('%.0f:%.2f'%(z,t) for z,t in row)))
print('TRIO3DONE')
