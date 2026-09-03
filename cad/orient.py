"""Which orientation should the crown print in?  Cheap: rotate the face normals
and sum the area that faces downward steeply enough to need support."""
import trimesh, numpy as np
from _occ import L
c = L('../VISAVERSE_v2/2_CROWN.3mf')
n = c.face_normals; a = c.area_faces; v = c.vertices
def score(R, name):
    nn = n @ R.T; vv = v @ R.T
    ext = vv.max(axis=0)-vv.min(axis=0)
    # support needed: normal more than 45 deg below horizontal
    need = nn[:,2] < -np.cos(np.radians(45.))
    steep = nn[:,2] < -np.cos(np.radians(60.))     # very steep, definitely support
    h = ext[2]
    foot = None
    fits = (max(ext[0],ext[1])<=350. and min(ext[0],ext[1])<=320. and ext[2]<=325.)
    print('  %-28s  %6.1f x %6.1f x %6.1f   overhang %7.1f mm2  steep %7.1f  aspect %4.1f %s'
          % (name, ext[0],ext[1],ext[2], a[need].sum(), a[steep].sum(),
             h/max(1e-6,min(ext[0],ext[1])), '' if fits else 'BED!'))
I = np.eye(3)
def rot(ax, deg):
    return trimesh.transformations.rotation_matrix(np.radians(deg), ax)[:3,:3]
print('crown orientations (as-modelled print z is the 268.40 axis):')
score(I, 'as modelled (standing)')
score(rot([0,1,0],90), 'lying, rotate Y 90')
score(rot([0,1,0],-90), 'lying, rotate Y -90')
score(rot([1,0,0],90) @ rot([0,1,0],90), 'lying, Y90 then X90')
score(rot([1,0,0],-90) @ rot([0,1,0],90), 'lying, Y90 then X-90')
score(rot([1,0,0],180) @ rot([0,1,0],90), 'lying, Y90 then X180')
for t in (30.,40.,50.):
    score(rot([1,0,0],t) @ rot([0,1,0],90), 'lying, Y90 then X%.0f' % t)
    score(rot([1,0,0],-t) @ rot([0,1,0],90), 'lying, Y90 then X-%.0f' % t)
print('ORDONE')
