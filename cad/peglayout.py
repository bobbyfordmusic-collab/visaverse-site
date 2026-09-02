"""Are the guide pegs continuous rails or discrete pegs, and where along the
door do they sit?"""
import trimesh, numpy as np
from _occ import L
for nm,fn in (('LOWER','4_SHUTTER_LOWER'),('UPPER','5_SHUTTER_UPPER')):
    d = L('../VISAVERSE_v2/%s.3mf'%fn)
    R = trimesh.ray.ray_triangle.RayMeshIntersector(d)
    y0,y1 = d.bounds[0][1], d.bounds[1][1]
    print('\n=== %s   y %.2f .. %.2f ===' % (nm,y0,y1))
    for side,x_probe,cmp_ in (('left',-129.5,'min'),('right',124.5,'max')):
        spans=[]; on=False; s=None
        for y in np.arange(y0+0.5, y1-0.5, 0.5):
            loc,_,_=R.intersects_location(np.array([[-300.,y,2.5]]),np.array([[1.,0.,0.]]),
                                          multiple_hits=True)
            if not len(loc): ext=None
            else: ext = loc[:,0].min() if side=='left' else loc[:,0].max()
            far = ext is not None and (ext < -130.5 if side=='left' else ext > 127.3)
            if far and not on: on=True; s=y
            if not far and on: on=False; spans.append((s,y-0.5))
        if on: spans.append((s,y1))
        print('  %-5s side: %d peg run(s) at door z=2.5' % (side,len(spans)))
        for a,b in spans: print('        y %7.2f .. %7.2f   (%.2f long)' % (a,b,b-a))
print('PLDONE')
