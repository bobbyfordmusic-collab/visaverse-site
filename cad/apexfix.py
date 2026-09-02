"""The crown's peg grooves were cut on a straight tangent where the track
actually curves.  Two consequences: the groove drifts outward and misses the
peg band (20.9..25.4) over theta 60..102, worst 4.10 mm at theta 84; and it
exits through the roof, severing it completely at theta 85..95.

Fix in two steps, both following the real arc (centre base y 110.12, z 247.94):
  1. RESTORE the roof - union back the original crown's material in the strips
     for r >= 27.9, so nothing can be added outside the original solid.
  2. CUT the groove properly - r 19.5..27.5 over theta 40..120, which covers the
     peg band with margin and blends into the straight legs at both ends.
"""
import trimesh, numpy as np
from shapely.geometry import Polygon
from _occ import L
MF='manifold'
T = np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]])
Tinv = np.linalg.inv(T)
CY, CZ = 110.12, 247.94
STRIPS = {'left':(-131.62,-129.50), 'right':(124.00,128.40)}
ROT = np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]])   # mesh(x,y,z) -> world(y,z,x)

def sector(r0, r1, t0, t1, x0, x1):
    th = np.radians(np.linspace(t0, t1, 160))
    pts = [(CY+r1*np.cos(t), CZ+r1*np.sin(t)) for t in th] + \
          [(CY+r0*np.cos(t), CZ+r0*np.sin(t)) for t in th[::-1]]
    m = trimesh.creation.extrude_polygon(Polygon(pts), height=x1-x0)
    M = np.eye(4); M[:3,:3]=ROT; M[:3,3]=[x0,0.,0.]
    m.apply_transform(M); return m

crown = L('CROWN_before_apex.3mf'); crown.apply_transform(T)
orig  = L('CROWN_before.3mf');      orig.apply_transform(T)
V0 = crown.volume
print('crown in : %.3f cm3, %d bodies, wt %s' % (V0/1000, len(crown.split(only_watertight=False)), crown.is_watertight))

# ---- 1. restore the roof --------------------------------------------------
fills=[]
for nm,(x0,x1) in STRIPS.items():
    s = sector(27.9, 40.0, 35., 145., x0, x1)
    f = trimesh.boolean.intersection([orig, s], engine=MF)
    v = 0. if f.is_empty else abs(f.volume)/1000
    print('  restore %-5s %.4f cm3' % (nm, v))
    if not f.is_empty: fills.append(f)
work = trimesh.boolean.union([crown]+fills, engine=MF)
print('after roof restore: %.3f cm3 (+%.3f)  wt %s'
      % (work.volume/1000, (work.volume-V0)/1000, work.is_watertight))

# ---- 2. cut the groove on the arc ----------------------------------------
cuts = [sector(19.5, 27.5, 40., 120., x0, x1) for x0,x1 in STRIPS.values()]
cut = trimesh.boolean.union(cuts, engine=MF)
# protect every dowel axis, as before
prot=[]
for bx,by in [(-126,108),(-126,124),(0,108),(0,126),(126,104),(124,124)]:
    cy_=trimesh.creation.cylinder(radius=4.0, height=20.0, sections=48)
    cy_.apply_translation([float(bx),float(by),247.0]); prot.append(cy_)
cut = trimesh.boolean.difference([cut]+prot, engine=MF)
V1 = work.volume
out = trimesh.boolean.difference([work, cut], engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
print('after groove cut  : %.3f cm3 (-%.3f)  bodies %d  wt %s'
      % (out.volume/1000, (V1-out.volume)/1000, len(parts), out.is_watertight))
out.apply_transform(Tinv)
b0 = L('CROWN_before_apex.3mf').bounds
print('print bounds delta %s' % np.round(np.abs(out.bounds-b0),5).tolist())
assert out.is_watertight and out.is_volume, 'crown not a valid solid'
assert len(parts)==1, 'crown split into %d bodies' % len(parts)
assert np.allclose(out.bounds, b0, atol=1e-6), 'outer bounds moved'
out.export('../VISAVERSE_v2/2_CROWN.3mf')
print('wrote 2_CROWN.3mf')
print('AFDONE')
