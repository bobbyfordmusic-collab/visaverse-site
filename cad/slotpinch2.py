"""Same scan, but a span only counts as the slot if it is walled on BOTH sides
in x - otherwise the picker just finds open air behind the base."""
import trimesh, numpy as np
from _occ import L
base = L('../VISAVERSE_v2/1_BASE.3mf')
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
print('base  bounds', np.round(base.bounds,2).tolist())
print('crown bounds (placed)', np.round(crown.bounds,2).tolist())
RB = trimesh.ray.ray_triangle.RayMeshIntersector(base)
RC = trimesh.ray.ray_triangle.RayMeshIntersector(crown)
NEED_BODY, NEED_PEG = 258.80, 260.02
LO, HI = -145., 145.

def solids(y, z):
    out=[]
    for r in (RB, RC):
        loc,_,_ = r.intersects_location(np.array([[-300.,y,z]]), np.array([[1.,0.,0.]]),
                                        multiple_hits=True)
        if not len(loc): continue
        xs = np.sort(np.round(loc[:,0], 5))
        xs = xs[np.concatenate([[True], np.diff(xs) > 1e-4])]
        if len(xs) % 2: xs = xs[:-1]
        out += [(xs[i], xs[i+1]) for i in range(0, len(xs), 2)]
    return sorted(out)

def walled_spans(y, z):
    """free intervals with solid on both sides"""
    sol = solids(y, z)
    if len(sol) < 2: return []
    merged=[list(sol[0])]
    for a,b in sol[1:]:
        if a <= merged[-1][1]+1e-6: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    return [(merged[i][1], merged[i+1][0]) for i in range(len(merged)-1)]

print('\n=== stow slot, walled spans only ===')
print('    z      y      free x span          width')
worst=(1e9,None)
for z in np.arange(176., 239.3, 3.0):
    best=(0.,None,None)
    for y in np.arange(126., 168.1, 0.5):
        for a,b in walled_spans(y,z):
            if b-a > best[0] and b-a > 100.: best=(b-a,y,(a,b))
    if best[1] is None:
        print('  %6.1f    --      no walled span > 100 mm' % z); continue
    w,y,(a,b)=best
    if w < worst[0]: worst=(w,z)
    print('  %6.1f  %6.1f   %8.2f..%8.2f  %8.2f%s'
          % (z,y,a,b,w, '   <<< under door body' if w < NEED_BODY else
                        ('   (peg-tight)' if w < NEED_PEG else '')))
print('\nnarrowest walled span in the slot: %.2f mm at z %.1f  (body %.2f, pegs %.2f)'
      % (worst[0], worst[1], NEED_BODY, NEED_PEG))
print('SP2DONE')
