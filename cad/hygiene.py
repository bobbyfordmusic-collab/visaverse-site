"""Coincident-face debris in the crown (a 283 mm2 zero-volume sheet at
x=-129.5 was reported before the apex re-cut).  Count opposite-normal face
pairs whose centroids nearly coincide."""
import trimesh, numpy as np
from scipy.spatial import cKDTree
from _occ import L
for f in ('2_CROWN','1_BASE','9_SILL_CAP','4_SHUTTER_LOWER'):
    m=L('../VISAVERSE_v2/%s.3mf'%f)
    c=m.triangles_center; n=m.face_normals; a=m.area_faces
    t=cKDTree(c); pairs=t.query_pairs(r=2e-4)
    sheet=0.; cnt=0
    for i,j in pairs:
        if np.dot(n[i],n[j])<-0.999 and abs(a[i]-a[j])<1e-6:
            sheet+=a[i]; cnt+=1
    zero=int((a<1e-8).sum())
    print('%-18s faces %7d  coincident opposite pairs %5d  sheet area %8.2f mm2  zero-area faces %d'
          % (f,len(m.faces),cnt,sheet,zero))
print('HYGDONE')
