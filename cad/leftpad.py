"""At the cap's correct placement (u = 0) its left pad reaches u -122.25,
0.375 mm inboard of the slab's edge at -122.625, and digs into the slab's
corner over the pad's 2.29 mm depth.  Trim the pad's inner edge back to
u -123.0 (0.375 clear).  Own-frame pads: w 27.687..29.937 under the cap's
underside at 29.937 - the cut stops at 29.90 so the bar is untouched."""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L, Ts, Tb
MF='manifold'; D='../VISAVERSE_v2/'
def vol(i): return 0. if i.is_empty else abs(i.volume)/1000
def bx(x0,x1,y0,y1,z0,z1):
    m=mk(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
cap=L('CAP_before_leftpad.3mf'); V0=cap.volume; B0=cap.bounds.copy()
cs=cap.copy(); cs.apply_transform(Ts)
out=trimesh.boolean.difference([cs, bx(-123.0,-119.0,-172.,-151.,24.0,29.90)],engine=MF)
out.apply_transform(Tb)
dv=(V0-out.volume)/1000
print('cap %.4f -> %.4f cm3 (removed %.4f)  bodies %d  wt %s  bounds moved %s'
      % (V0/1000,out.volume/1000,dv,len(out.split(only_watertight=False)),out.is_watertight,
         not np.allclose(out.bounds,B0,atol=1e-6)))
assert out.is_watertight and 0.0<dv<0.05
out.export(D+'9_SILL_CAP.3mf')
# verify at u = 0
c=L(D+'9_SILL_CAP.3mf'); c.apply_transform(Ts); c.apply_translation([0.,93.063,139.45-29.937])
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
us=np.arange(-140.,132.01,0.05)
P=np.column_stack([us,np.full(len(us),-69.0),np.full(len(us),138.2)])
s=sol(c,P); r=[];st=None
for i,v in enumerate(s):
    if v and st is None: st=i
    if not v and st is not None: r.append((us[st],us[i-1])); st=None
print('pads at u=0, w 138.2 : %s   (slab edge -122.625)' % '  '.join('%.2f..%.2f'%q for q in r))
c.apply_transform(Tb)
slab=L(D+'6_TABLET_SLAB.3mf'); slab.apply_translation([0.,98.,133.6]); slab.apply_transform(Tb)
i=trimesh.boolean.intersection([c,slab],engine=MF); j=i.copy(); j.apply_transform(Ts); b=j.bounds
print('cap(u=0) ^ slab now : %.5f cm3   w %.3f..%.3f  (film only if w starts at 139.45)'
      % (vol(i),b[0][2],b[1][2]))
base=L(D+'1_BASE.3mf')
print('cap(u=0) ^ base     : %.5f cm3' % vol(trimesh.boolean.intersection([c,base],engine=MF)))
print('LPDONE')
