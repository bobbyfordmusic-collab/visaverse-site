"""Trim the sill cap's right-hand pad clear of the slab.

The cap's underside is flat at w 29.937 (its own slope frame) except two pads
that drop to 27.687 over the front 8.50 mm.  Seated, the right pad runs from
u 115.20 outward, but the slab's edge is at u +122.625 - so the pad overlapped
the slab's front-right corner by 7.4 mm wide and up to 2.29 mm deep.

The pad is cut back to u 123.00 seated (= 123.453 in the cap's own frame),
which is 0.375 mm outboard of the slab's edge.  9.3 mm of pad is left.
The left pad ends at -122.20 seated and already clears the slab's -122.625 edge.
"""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L, Ts, Tb
MF='manifold'
DU = -0.453                      # cap's own u -> seated u
U0, U1 = 114.0, 123.00 - DU      # own-frame band to remove
W0, W1 = 26.50, 29.94            # pad depth, just into the seat face
V0, V1 = -168.0, -155.0

c = L('CAP_before.3mf'); P0, V_0 = c.bounds.copy(), c.volume
print('cap in : %.3f cm3  bounds %s' % (V_0/1000, np.round(P0,3).tolist()))
cs = c.copy(); cs.apply_transform(Ts)
cut = mk(extents=[U1-U0, V1-V0, W1-W0])
cut.apply_translation([(U0+U1)/2, (V0+V1)/2, (W0+W1)/2])
out = trimesh.boolean.difference([cs, cut], engine=MF)
parts = sorted(out.split(only_watertight=False), key=lambda q:-abs(q.volume))
if len(parts) > 1:
    lost = sum(abs(p.volume) for p in parts[1:])/1000
    print('freed %d island(s), %.4f cm3' % (len(parts)-1, lost))
    assert lost < 0.05, 'freed %.3f cm3' % lost
    out = parts[0]
out.apply_transform(Tb)
d = (V_0-out.volume)/1000
print('cap out: %.3f cm3  removed %.4f cm3  wt %s  bodies %d'
      % (out.volume/1000, d, out.is_watertight, len(out.split(only_watertight=False))))
print('bounds delta %s' % np.round(np.abs(out.bounds-P0),4).tolist())
assert out.is_watertight, 'not watertight'
assert np.allclose(out.bounds, P0, atol=1e-6), 'cap outer bounds moved'
assert 0.05 < d < 0.60, 'removed %.4f cm3' % d
out.export('../VISAVERSE_v2/9_SILL_CAP.3mf')
print('wrote 9_SILL_CAP.3mf')
