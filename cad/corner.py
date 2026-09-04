"""1. With the left panel door fitted, is the slot's bottom-left corner closed?
   2. Where does the stow slot actually end (search further down / forward)?"""
import trimesh, numpy as np
from _occ import L
base=L('../VISAVERSE_v2/1_BASE.3mf')
lpd=L('../VISAVERSE_v2/3_LEFT_PANEL_DOOR.3mf'); lpd.apply_transform(
    np.array([[0.,0.,1.,-135.60],[1.,0.,0.,0.065],[0.,1.,0.,144.00],[0,0,0,1.]]))
RB=trimesh.ray.ray_triangle.RayMeshIntersector(base)
RD=trimesh.ray.ray_triangle.RayMeshIntersector(lpd)
def solids(R,y,z):
    loc,_,_=R.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
    if not len(loc): return []
    xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
    if len(xs)%2: xs=xs[:-1]
    return [(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
def gaps(y,z,with_door):
    s=sorted(solids(RB,y,z)+(solids(RD,y,z) if with_door else []))
    if len(s)<2: return []
    m=[list(s[0])]
    for a,b in s[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return [(m[i][1],m[i+1][0]) for i in range(len(m)-1) if m[i+1][0]-m[i][1]>100.]
print('=== 1. slot bottom-left corner, base alone vs base + fitted panel door ===')
print('   z    y     base only                  base + door')
for z in (37.,39.,41.):
    for y in (108.,112.,116.):
        g0=gaps(y,z,False); g1=gaps(y,z,True)
        f=lambda g: '  '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in g) or 'no walled span'
        print('  %4.0f  %4.0f   %-26s  %s' % (z,y,f(g0),f(g1)))
print('\n=== 2. where does the slot end?  widest walled span (base+door) by z, y searched 40..130 ===')
for z in np.arange(16.,44.1,4.):
    best=(0.,None,None)
    for y in np.arange(40.,130.01,0.5):
        for a,b in gaps(y,z,True):
            if b-a>best[0]: best=(b-a,y,(a,b))
    print('  z %4.0f : %s' % (z, ('%.2f at y %.1f (%.2f/%.2f)'%(best[0],best[1],*best[2])) if best[1] else 'none'))
print('CORNERDONE')
