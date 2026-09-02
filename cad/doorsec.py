"""The lower door's cross-section: body width vs peg width, and where in the
door's thickness the pegs sit."""
import trimesh, numpy as np
from _occ import L
lo = L('../VISAVERSE_v2/4_SHUTTER_LOWER.3mf')
up = L('../VISAVERSE_v2/5_SHUTTER_UPPER.3mf')
CW = 141.85-(0.05+6.30)/2.
for nm,d in (('LOWER',lo),('UPPER',up)):
    print('\n=== %s  print bounds %s ===' % (nm, np.round(d.bounds,3).tolist()))
    R = trimesh.ray.ray_triangle.RayMeshIntersector(d)
    print('   z (door)   w (slope)      x extent of material        width')
    for z in np.arange(0.25, d.bounds[1][2], 0.5):
        # cast along x at several y to find the widest material extent
        xs=[]
        for y in np.arange(d.bounds[0][1]+2., d.bounds[1][1]-2., 3.0):
            loc,_,_=R.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),
                                          multiple_hits=True)
            if len(loc): xs += [loc[:,0].min(), loc[:,0].max()]
        if not xs: print('  %7.2f   %7.2f     (nothing)'%(z,z+CW)); continue
        print('  %7.2f   %7.2f   %8.2f..%8.2f   %8.2f'
              % (z, z+CW, min(xs), max(xs), max(xs)-min(xs)))
print('DSDONE')
