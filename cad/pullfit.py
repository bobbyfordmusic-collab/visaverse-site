"""Place the door pull on the lower shutter door and check the whole chain."""
import trimesh, numpy as np
from _occ import L, Tb, Ts
MF='manifold'
def vol(i): return 0.0 if i.is_empty else abs(i.volume)/1000
lo   = L('../VISAVERSE_v2/4_SHUTTER_LOWER.3mf')
pull = L('../VISAVERSE_v2/8_DOOR_PULL.3mf')
# pull -> door frame: flip about x, then translate
M = np.eye(4); M[:3,:3] = np.diag([1.,-1.,-1.]); M[:3,3] = [-2.775, 0.825, 3.60]
pull.apply_transform(M)
print('pull in the door frame: bounds %s' % np.round(pull.bounds,3).tolist())
print('  pegs should sit in the door sockets at x -32.70 / +27.30, y 0.75, 7.10 deep')
print('\npull ^ lower door : %.5f cm3' % vol(trimesh.boolean.intersection([pull, lo], engine=MF)))
base = L('../VISAVERSE_v2/1_BASE.3mf')
cap  = L('../VISAVERSE_v2/9_SILL_CAP.3mf'); cap.apply_transform(Ts)
cap.apply_translation([-0.453, 93.063, 139.45-29.937]); cap.apply_transform(Tb)
Rm = np.array([[0.,0.,-1.],[0.,1.,0.],[1.,0.,0.]])
Tc = np.eye(4); Tc[:3,:3]=Rm; Tc[:3,3]=[132.30, 99.30, 259.5347]
crown = L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(Tc)
asm = trimesh.boolean.union([base, crown], engine=MF)
CW = 141.85-(0.05+6.30)/2.
print('\ndoor + pull through the travel, vs base+crown and vs the sill cap:')
for cv in (-63., -50., -30., 0., 30., 60.):
    q = pull.copy(); q.apply_translation([0., cv, CW]); q.apply_transform(Tb)
    print('   cv=%6.1f : ^ base+crown %8.4f   ^ sill cap %8.4f'
          % (cv, vol(trimesh.boolean.intersection([q, asm], engine=MF)),
                 vol(trimesh.boolean.intersection([q, cap], engine=MF))))
