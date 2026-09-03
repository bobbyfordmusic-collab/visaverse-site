"""Sill cap at its corrected placement (u = 0) against the closed lower door,
the seated slab, and the pull - only base/crown were checked at u = 0."""
import trimesh, numpy as np
from _occ import L, Ts, Tb
MF='manifold'; D='../VISAVERSE_v2/'
def vol(i): return 0. if i.is_empty else abs(i.volume)/1000
def bnd(i):
    if i.is_empty: return ''
    j=i.copy(); j.apply_transform(Ts); b=j.bounds
    return ' slope u %.2f..%.2f v %.2f..%.2f w %.3f..%.3f'%(b[0][0],b[1][0],b[0][1],b[1][1],b[0][2],b[1][2])
cap=L(D+'9_SILL_CAP.3mf'); cap.apply_transform(Ts)
cap.apply_translation([0.0,93.063,139.45-29.937]); cap.apply_transform(Tb)
lo=L(D+'4_SHUTTER_LOWER.3mf'); CW=138.675
pull=L(D+'8_DOOR_PULL.3mf')
M=np.eye(4); M[:3,:3]=np.diag([1.,-1.,-1.]); M[:3,3]=[-2.775,0.825,3.60]; pull.apply_transform(M)
slab=L(D+'6_TABLET_SLAB.3mf'); slab.apply_translation([0.,98.,133.6]); slab.apply_transform(Tb)
i=trimesh.boolean.intersection([cap,slab],engine=MF)
print('cap(u=0) ^ slab        : %.5f cm3%s' % (vol(i),bnd(i)))
for cv in (-55.949,-55.749,-50.):
    d=lo.copy(); d.apply_translation([0.,cv,CW]); d.apply_transform(Tb)
    p=pull.copy(); p.apply_translation([0.,cv,CW]); p.apply_transform(Tb)
    i=trimesh.boolean.intersection([cap,d],engine=MF)
    print('cap(u=0) ^ lower cv %.3f: %.5f cm3%s' % (cv,vol(i),bnd(i)))
    print('cap(u=0) ^ pull  cv %.3f: %.5f cm3' % (cv,vol(trimesh.boolean.intersection([cap,p],engine=MF))))
# where do the cap's ends sit relative to the base's outer faces?
b=cap.bounds; print('cap placed x %.3f..%.3f  (base outer -136.100..132.300)'%(b[0][0],b[1][0]))
print('CAPDONE')
