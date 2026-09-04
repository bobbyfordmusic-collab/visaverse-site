"""Definitive path check: at every station along the door's run, compare the
clear span against the door's ACTUAL width at that height in its section.

lower door section (w = door z + 138.675):
  138.675..140.42  body underside   253.20
  140.42 ..143.92  guide pegs       258.80
  143.92 ..144.92                   249.50
  144.92 ..147.48  raised back      240.57
"""
import trimesh, numpy as np
from _occ import L, Tb
base = L('../VISAVERSE_v2/1_BASE.3mf')
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
RB=trimesh.ray.ray_triangle.RayMeshIntersector(base)
RC=trimesh.ray.ray_triangle.RayMeshIntersector(crown)
PROFILE=[(139.0,140.3,253.20),(140.6,143.8,258.80),(144.1,144.8,249.50),(145.1,147.3,240.57)]
def widest(y,z):
    sol=[]
    for r in (RB,RC):
        loc,_,_=r.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
        if not len(loc): continue
        xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
        if len(xs)%2: xs=xs[:-1]
        sol+=[(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
    sol=sorted(sol)
    if len(sol)<2: return None
    m=[list(sol[0])]
    for a,b in sol[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    gaps=[(m[i][1],m[i+1][0]) for i in range(len(m)-1)]
    gaps=[g for g in gaps if g[1]-g[0]>100.]
    return max(gaps,key=lambda g:g[1]-g[0]) if gaps else None
print('  slope v   tightest band      clear     need     margin')
worst=(1e9,None)
for v in np.arange(120., 282.1, 4.0):
    tight=(1e9,None,None,None)
    for w0,w1,need in PROFILE:
        for w in np.arange(w0,w1+1e-9,0.55):
            p=trimesh.transform_points([[0.,v,w]],Tb)[0]
            g=widest(p[1],p[2])
            clear=(g[1]-g[0]) if g else 0.
            if clear-need < tight[0]: tight=(clear-need,w,clear,need)
    marg,w,clear,need=tight
    if marg<worst[0]: worst=(marg,v)
    print('  %7.1f   w %6.2f          %8.2f %8.2f  %+8.2f%s'
          % (v,w,clear,need,marg,'   <<<' if marg<0 else ''))
print('\nworst margin %.2f mm at v %.1f' % worst)
print('PSDONE')
