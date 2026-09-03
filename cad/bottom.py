"""Slot bottom, z 36..50, with the merged-solids walled-span method
(the one that gave 260.37 at z 40 before the wedge fill).  Also report the
slot's y-band against the wedge-fill box (y 97..105.4, z 40.97..43.66)."""
import trimesh, numpy as np
from _occ import L
base=L('../VISAVERSE_v2/1_BASE.3mf')
R=trimesh.ray.ray_triangle.RayMeshIntersector(base)
def walled(y,z):
    loc,_,_=R.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
    if not len(loc): return []
    xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
    if len(xs)%2: xs=xs[:-1]
    s=[(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
    m=[list(s[0])]
    for a,b in s[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return [(m[i][1],m[i+1][0]) for i in range(len(m)-1) if m[i+1][0]-m[i][1]>100.]
print('   z    slot y-band (>=258.8 spans)   widest span        at y')
for z in np.arange(36.,50.1,2.):
    ys=[];best=(0.,None,None)
    for y in np.arange(90.,126.01,0.25):
        for a,b in walled(y,z):
            if b-a>=258.8: ys.append(y)
            if b-a>best[0]: best=(b-a,y,(a,b))
    band='%.2f..%.2f'%(min(ys),max(ys)) if ys else 'none'
    print('  %5.0f   %-28s %8.2f  (%.2f/%.2f)  y %.2f%s'
          % (z,band,best[0],best[2][0],best[2][1],best[1],'' if best[0]>=258.8 else '  <<<'))
print('wedge fill occupied y 97.0..105.4, z 40.97..43.66 - the band above must stay clear of it')
print('BOTDONE')
