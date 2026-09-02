"""Full y-band of the crown's return leg at each height, plus the crown's dowel
bores, to see whether a widening cut can clear them."""
import trimesh, numpy as np
from _occ import L
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
base = L('../VISAVERSE_v2/1_BASE.3mf')
RB=trimesh.ray.ray_triangle.RayMeshIntersector(base)
RC=trimesh.ray.ray_triangle.RayMeshIntersector(crown)
print('crown placed bounds', np.round(crown.bounds,2).tolist())
def gaps(y,z):
    sol=[]
    for r in (RB,RC):
        loc,_,_=r.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
        if not len(loc): continue
        xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
        if len(xs)%2: xs=xs[:-1]
        sol+=[(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
    sol=sorted(sol)
    if len(sol)<2: return []
    m=[list(sol[0])]
    for a,b in sol[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return [(m[i][1],m[i+1][0]) for i in range(len(m)-1) if m[i+1][0]-m[i][1] > 200.]
print('\n=== return leg y-band per height ===')
print('    z     y lo    y hi   thick   x span               width')
for z in np.arange(239.5, 276.1, 1.5):
    rows=[]
    for y in np.arange(108., 148.1, 0.25):
        for a,b in gaps(y,z): rows.append((y,a,b,b-a))
    if not rows: print('  %6.1f   (none)'%z); continue
    ys=[r[0] for r in rows]; best=max(rows,key=lambda r:r[3])
    print('  %6.1f  %6.2f  %6.2f  %5.2f  %8.2f..%8.2f  %8.2f%s'
          % (z,min(ys),max(ys),max(ys)-min(ys),best[1],best[2],best[3],
             '   <<<' if best[3]<258.80 else ''))
print('\n=== crown dowel bores: x extent near the right strip ===')
for (bx,by) in [(126,104),(124,124),(0,108),(0,126),(-126,108),(-126,124)]:
    for z in (242., 248., 253.):
        loc,_,_=RC.intersects_location(np.array([[-300.,float(by),z]]),
                                       np.array([[1.,0.,0.]]),multiple_hits=True)
        if not len(loc): continue
        xs=np.sort(np.round(loc[:,0],5))
        near=[x for x in xs if abs(x-bx)<6.]
        if near: print('  bore (%5d,%4d) z %.0f  surfaces at x %s'
                       % (bx,by,z,' '.join('%.2f'%x for x in near)))
print('RLDONE')
