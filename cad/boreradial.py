"""Radial probe: from each bore axis, shoot rays outward in 36 directions.
An intact bore returns 3.20 in every direction."""
import trimesh, numpy as np
from _occ import L
T = np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]])
POS = [(-126,108),(-126,124),(0,108),(0,126),(126,104),(124,124)]
ANG = np.radians(np.arange(0,360,10.))
DIRS = np.column_stack([np.cos(ANG), np.sin(ANG), np.zeros(len(ANG))])
for tag,fn in (('BEFORE','CROWN_before.3mf'), ('NOW','../VISAVERSE_v2/2_CROWN.3mf')):
    c = L(fn); c.apply_transform(T)
    R = trimesh.ray.ray_triangle.RayMeshIntersector(c)
    print('\n=== %s ===' % tag)
    print('  bore            z=242              z=248              z=252')
    for bx,by in POS:
        cells=[]
        for z in (242.,248.,252.):
            org = np.tile([float(bx),float(by),z],(len(DIRS),1))
            loc,idx,_ = R.intersects_location(org, DIRS, multiple_hits=False)
            if not len(loc): cells.append('  no wall '); continue
            r = np.linalg.norm(loc[:,:2]-np.array([bx,by]), axis=1)
            miss = len(DIRS)-len(np.unique(idx))
            breached = int((r > 4.0).sum())
            cells.append('%.2f..%-6.2f %s' % (r.min(), r.max(),
                         ('OK ' if r.max()<4.0 else 'BREACH x%d'%breached)))
        print('  (%5d,%4d)  %s' % (bx,by,'  '.join('%-18s'%c for c in cells)))
print('BRDONE')
