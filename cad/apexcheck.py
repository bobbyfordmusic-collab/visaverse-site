"""Independent check of the reported apex blockage, by point containment only.

Arc centre reported at base (y,z) = (110.12, 247.94), outer R 31.77.
My angle convention: theta measured in the (y,z) plane from +y toward +z, so
point = (x, cy + r cos t, cz + r sin t).  theta 90 = apex.  Slope leg ~166 deg,
return leg ~6 deg.
"""
import trimesh, numpy as np
from _occ import L
CY, CZ = 110.12, 247.94
crown = L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
def solid(pts):
    pts=np.asarray(pts,float); out=np.zeros(len(pts),bool)
    for i in range(0,len(pts),3000): out[i:i+3000]=crown.contains(pts[i:i+3000])
    return out
TH = np.arange(30., 151., 6.)
RR = np.arange(18.0, 28.51, 0.25)
LANES = {'main  x=0':[0.], 'left strip':[-131.0,-130.5,-130.0], 'right strip':[124.6,126.0,127.8]}
res={}
for nm,xs in LANES.items():
    P=[]; idx=[]
    for t in TH:
        for r in RR:
            y = CY + r*np.cos(np.radians(t)); z = CZ + r*np.sin(np.radians(t))
            for x in xs: P.append([x,y,z]); idx.append((t,r))
    s = solid(P)
    # a (t,r) cell counts as void only if EVERY x sample in the lane is void
    d={}
    for (t,r),v in zip(idx,s): d[(t,r)] = d.get((t,r),True) and (not v)
    res[nm]=d
print('void radial band in each lane   (theta 90 = apex, 166 = slope leg, 6 = return leg)')
print(' theta |      main channel      |      left strip       |      right strip')
for t in TH:
    cells=[]
    for nm in LANES:
        rs=[r for r in RR if res[nm][(t,r)]]
        cells.append('%5.2f..%5.2f (%4.2f)'%(min(rs),max(rs),max(rs)-min(rs)) if rs else '      none        ')
    print(' %5.1f | %s | %s | %s' % (t, cells[0], cells[1], cells[2]))
print()
print('door pegs need r 20.9..25.4 (agent figure).  Blocked where a strip lane')
print('does not cover that band:')
bad=[]
for t in TH:
    for nm in ('left strip','right strip'):
        rs=[r for r in RR if res[nm][(t,r)]]
        if not rs: bad.append((t,nm,'no opening at all')); continue
        lo,hi=min(rs),max(rs)
        blocked = max(0., lo-20.9) + max(0., 25.4-hi)
        if blocked > 0.3: bad.append((t,nm,'open %.2f..%.2f -> %.2f mm of the peg blocked'%(lo,hi,blocked)))
for t,nm,msg in bad: print('   theta %5.1f  %-12s %s' % (t,nm,msg))
if not bad: print('   none - pegs clear all the way round')
print('APEXDONE')
