"""Exact footprint of the stow slot, and what material sits in the two strips
that would have to come out to widen it."""
import trimesh, numpy as np
from _occ import L
base = L('../VISAVERSE_v2/1_BASE.3mf')
RB = trimesh.ray.ray_triangle.RayMeshIntersector(base)
def solids(y,z):
    loc,_,_ = RB.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
    if not len(loc): return []
    xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
    if len(xs)%2: xs=xs[:-1]
    return sorted([(xs[i],xs[i+1]) for i in range(0,len(xs),2)])
def walled(y,z):
    sol=solids(y,z)
    if len(sol)<2: return []
    m=[list(sol[0])]
    for a,b in sol[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return [(m[i][1],m[i+1][0]) for i in range(len(m)-1)]
print('=== slot footprint (y band of the >100mm walled span) ===')
print('    z     y lo    y hi   thick    width')
rows=[]
for z in np.arange(20., 240.1, 4.0):
    ys=[]; wmax=0.
    for y in np.arange(95.,170.1,0.25):
        for a,b in walled(y,z):
            if b-a>100.: ys.append(y); wmax=max(wmax,b-a)
    if not ys: print('  %6.1f   (none)' % z); continue
    rows.append((z,min(ys),max(ys),wmax))
    print('  %6.1f  %6.2f  %6.2f  %6.2f  %7.2f%s'
          % (z,min(ys),max(ys),max(ys)-min(ys),wmax,'   <<<' if wmax<258.8 else ''))
if rows:
    zs=[r[0] for r in rows]
    print('\nslot runs z %.1f .. %.1f' % (min(zs), max(zs)))
    lo=[r for r in rows if r[3]<258.8]
    if lo: print('narrow (253.50) over z %.1f .. %.1f' % (min(r[0] for r in lo), max(r[0] for r in lo)))
print('SFDONE')
