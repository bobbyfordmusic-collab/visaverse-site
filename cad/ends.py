"""The 11 end-station 'fails': re-scan those heights locating the slot by
searching y for the widest walled span, base+crown together."""
import trimesh, numpy as np
from _occ import L
base=L('../VISAVERSE_v2/1_BASE.3mf')
crown=L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
def solid(P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),1500):
        q=P[i:i+1500]; o[i:i+1500]=base.contains(q)|crown.contains(q)
    return o
XL=np.arange(-135.,-124.99,0.05); XR=np.arange(122.,132.01,0.05)
def span(y,z):
    sL=solid([[x,y,z] for x in XL]); sR=solid([[x,y,z] for x in XR])
    li=np.where(sL)[0]; ri=np.where(sR)[0]
    if not len(li) or not len(ri): return None
    return XL[li[-1]], XR[ri[0]]
print('   z     slot y (searched)   walls              span')
for z in (236.,229.,222.,47.,40.):
    best=None
    for y in np.arange(95.,165.01,0.5):
        r=span(y,z)
        if r and (best is None or r[1]-r[0]>best[2]): best=(y,r,r[1]-r[0])
    if best: print('  %5.0f   y %6.1f             %.2f / %.2f    %.2f %s'
                   % (z,best[0],best[1][0],best[1][1],best[2],'' if best[2]>=258.8 else '<<<'))
    else: print('  %5.0f   no walled span' % z)
print('ENDSDONE')
