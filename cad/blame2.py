"""Which edit closed the slot bottom?  Widest walled span at z 38/40/42 across
the slot band, for the base at each snapshot."""
import trimesh, numpy as np
from _occ import L
SNAPS=[('after slotdeep (BASE_before_trio)','BASE_before_trio.3mf'),
       ('after pilot   (BASE_before_skin)','BASE_before_skin.3mf'),
       ('after membrane(BASE_before_wedge)','BASE_before_wedge.3mf'),
       ('NOW','../VISAVERSE_v2/1_BASE.3mf')]
def walled(R,y,z):
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
for nm,f in SNAPS:
    R=trimesh.ray.ray_triangle.RayMeshIntersector(L(f))
    row=[]
    for z in (38.,40.,42.,44.):
        best=(0.,None)
        for y in np.arange(100.,126.01,0.5):
            for a,b in walled(R,y,z):
                if b-a>best[0]: best=(b-a,y)
        row.append('z%2.0f %6.2f@y%5.1f'%(z,best[0],best[1] if best[1] else 0))
    print('  %-36s %s' % (nm,' | '.join(row)))
print('BL2DONE')
