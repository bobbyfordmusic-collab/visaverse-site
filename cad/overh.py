"""Crown overhangs in PRINT orientation (the file is already in print coords:
40.52 x 88.78 x 268.40, printed standing on its z=0 end).
Find downward-facing faces that would need support, by area and height."""
import trimesh, numpy as np
from _occ import L
c = L('../VISAVERSE_v2/2_CROWN.3mf')
print('print bounds', np.round(c.bounds,2).tolist())
n = c.face_normals; a = c.area_faces
zc = c.triangles_center[:,2]
down = n[:,2] < -0.70            # within ~45 deg of straight down
print('\ndownward-facing area (needs support at a 45 deg threshold): %.0f mm2'
      % a[down].sum())
# cluster by height
print('\n   z band      area mm2   min-normal-z   note')
for z0 in np.arange(0., 270., 15.):
    m = down & (zc>=z0) & (zc<z0+15.)
    if a[m].sum() < 20: continue
    print('  %5.0f..%5.0f   %8.1f      %6.2f' % (z0, z0+15., a[m].sum(), n[m][:,2].min()))
# the big flat ceilings
flat = n[:,2] < -0.98
print('\nflat (horizontal) ceilings over 50 mm2, by height:')
groups={}
for i in np.where(flat)[0]:
    key = round(zc[i],1)
    groups[key] = groups.get(key,0.)+a[i]
for k in sorted(groups, reverse=True):
    if groups[k] > 50:
        m = flat & (np.abs(zc-k)<0.15)
        t = c.triangles[m].reshape(-1,3)
        print('   z %7.2f  area %7.1f mm2   x %7.2f..%7.2f  y %7.2f..%7.2f'
              % (k, groups[k], t[:,0].min(), t[:,0].max(), t[:,1].min(), t[:,1].max()))
print('OHDONE')
