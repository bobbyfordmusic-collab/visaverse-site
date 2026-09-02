"""Closed position = the door's bottom edge bumping the sill cap face.
Cap face (max v over the door's w band) is at v -62.949; the door's bottom edge
is its own y=-7, so contact is at cv = -55.949.  Verify the magnets meet there
and nothing else fouls."""
import trimesh, numpy as np
from _occ import L, Tb, Ts
MF='manifold'
def vol(i): return 0.0 if i.is_empty else abs(i.volume)/1000

lo   = L('../VISAVERSE_v2/4_SHUTTER_LOWER.3mf')
up   = L('../VISAVERSE_v2/5_SHUTTER_UPPER.3mf')
pull = L('../VISAVERSE_v2/8_DOOR_PULL.3mf')
M = np.eye(4); M[:3,:3]=np.diag([1.,-1.,-1.]); M[:3,3]=[-2.775,0.825,3.60]
pull.apply_transform(M)
capS = L('../VISAVERSE_v2/9_SILL_CAP.3mf'); capS.apply_transform(Ts)
capS.apply_translation([-0.453, 93.063, 139.45-29.937])
cap = capS.copy(); cap.apply_transform(Tb)
base = L('../VISAVERSE_v2/1_BASE.3mf')
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
slab = L('../VISAVERSE_v2/6_TABLET_SLAB.3mf'); slab.apply_translation([0.,98.,133.6])
slab.apply_transform(Tb)
CW = 141.85-(0.05+6.30)/2.
CV_STOP = -55.949

# --- magnet pockets on the door's bottom edge -------------------------------
v = lo.vertices
edge = v[v[:,1] < -6.0]
print('door bottom-edge verts %d, y %.3f..%.3f' % (len(edge), edge[:,1].min(), edge[:,1].max()))
for sgn in (-1,1):
    s = edge[np.sign(edge[:,0])==sgn]
    s = s[np.abs(np.abs(s[:,0])-55.)<8.]
    if len(s):
        print('  pocket x %8.3f..%8.3f  y %7.3f..%7.3f  z %6.3f..%6.3f'
              % (s[:,0].min(), s[:,0].max(), s[:,1].min(), s[:,1].max(), s[:,2].min(), s[:,2].max()))
# --- magnet recesses on the cap's facing face -------------------------------
cv_ = capS.vertices
face = cv_[(cv_[:,1] > -66.5) & (cv_[:,2] > 139.)]
for sgn in (-1,1):
    s = face[(np.sign(face[:,0])==sgn) & (np.abs(np.abs(face[:,0])-55.)<8.)]
    if len(s):
        print('  cap recess u %8.3f..%8.3f  v %7.3f..%7.3f  w %7.3f..%7.3f'
              % (s[:,0].min(), s[:,0].max(), s[:,1].min(), s[:,1].max(), s[:,2].min(), s[:,2].max()))

print('\n  cv        ^cap     ^base    ^crown    ^slab   pull^cap  pull^base')
for cv in [CV_STOP-0.2, CV_STOP, CV_STOP+0.2, CV_STOP+1.0, CV_STOP+5.0]:
    d = lo.copy(); d.apply_translation([0.,cv,CW]); d.apply_transform(Tb)
    u = up.copy(); u.apply_translation([0.,cv,CW]); u.apply_transform(Tb)
    p = pull.copy(); p.apply_translation([0.,cv,CW]); p.apply_transform(Tb)
    dd = trimesh.util.concatenate([d,u])
    print('  %7.3f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f  %7.4f' % (cv,
        vol(trimesh.boolean.intersection([d,cap],engine=MF)),
        vol(trimesh.boolean.intersection([dd,base],engine=MF)),
        vol(trimesh.boolean.intersection([dd,crown],engine=MF)),
        vol(trimesh.boolean.intersection([dd,slab],engine=MF)),
        vol(trimesh.boolean.intersection([p,cap],engine=MF)),
        vol(trimesh.boolean.intersection([p,base],engine=MF))))
print('done')
