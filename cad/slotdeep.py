"""The stow slot was only widened over its top 58 mm (z 178..236).  Below that,
z 36..176 - the bottom 70% of the slot - it is still 253.50 against a 258.80
door body, so the shutter enters the slot and jams 58 mm down.

The slot is a 9.11 mm slab tilted 10.02 deg from vertical: centre plane
N.(y,z) = 111.28 with N = (0, 0.9848, -0.1740), running along
D = (0, 0.1740, 0.9848).  The two wall strips are cut in that frame so the new
opening blends into the already-widened part with no step.

Walls left behind: 4.48 mm left, 3.90 mm right - identical to the upper region
that already prints.
"""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L
MF='manifold'
N = np.array([0., 0.9848, -0.1740]); D = np.array([0., 0.1740, 0.9848])
C_N, D0, D1 = 111.28, 55., 210.
STRIPS = {'left': (-131.62, -129.50), 'right': (124.00, 128.40)}
N_HALF = 6.5

base = L('BASE_before_slotdeep.3mf')
V0, B0 = base.volume, base.bounds.copy()
n0 = len(base.split(only_watertight=False))
print('base in : %.3f cm3, %d bodies, wt %s' % (V0/1000, n0, base.is_watertight))

R = np.column_stack([np.array([1.,0,0]), N, D])
cuts = []
for nm,(x0,x1) in STRIPS.items():
    m = mk(extents=[x1-x0, 2*N_HALF, D1-D0])
    T = np.eye(4); T[:3,:3] = R
    T[:3,3] = np.array([(x0+x1)/2., 0., 0.]) + C_N*N + ((D0+D1)/2.)*D
    m.apply_transform(T)
    b = m.bounds
    print('  %-5s strip x %8.2f..%8.2f  y %7.2f..%7.2f  z %7.2f..%7.2f'
          % (nm, b[0][0],b[1][0], b[0][1],b[1][1], b[0][2],b[1][2]))
    cuts.append(m)

out = trimesh.boolean.difference([base]+cuts, engine=MF)
parts = sorted(out.split(only_watertight=False), key=lambda p: -abs(p.volume))
parts = [p for p in parts if abs(p.volume) > 1.0]
out = trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
n1 = len(parts)
dv = (V0-out.volume)/1000
print('\nbase out: %.3f cm3  removed %.3f cm3  bodies %d  wt %s'
      % (out.volume/1000, dv, n1, out.is_watertight))
print('bounds delta %s' % np.round(np.abs(out.bounds-B0), 5).tolist())
assert out.is_watertight, 'base not watertight'
assert n1 == n0, 'body count %d -> %d (the cut severed structure)' % (n0, n1)
assert np.allclose(out.bounds, B0, atol=1e-6), 'outer bounds moved'
assert 12.0 < dv < 18.0, 'removed %.3f cm3, expected ~13.9' % dv
out.export('../VISAVERSE_v2/1_BASE.3mf')
print('wrote 1_BASE.3mf')
print('SDDONE')
