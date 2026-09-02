"""The 0.235 mm left-flank skin: is it mine, and what is behind it?"""
import trimesh, numpy as np
from _occ import L
FILES=[('now','../VISAVERSE_v2/1_BASE.3mf'),
       ('pre-slotdeep','BASE_before_slotdeep.3mf'),
       ('pre-stow','BASE_before_stow.3mf')]
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
def runs(mask,ax):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: out.append((ax[s],ax[i-1])); s=None
    if s is not None: out.append((ax[s],ax[-1]))
    return out
for nm,f in FILES:
    m=L(f)
    print('--- %s ---' % nm)
    for y,z in ((108.,40.),(112.,40.),(116.,36.),(120.,40.),(112.,55.)):
        xs=np.arange(-137.,-117.99,0.01)
        P=np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
        r=runs(sol(m,P),xs)
        print('   y %5.1f z %5.1f : %s' % (y,z,
              '  '.join('%.3f..%.3f (%.3f)'%(a,b,b-a) for a,b in r) or 'none'))
print('FLANKDONE')
