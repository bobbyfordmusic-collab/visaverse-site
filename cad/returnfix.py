"""The crown carries the door round the top on two legs: the slope leg (already
260.02) and the RETURN leg that hands off into the base's stow slot.  The return
leg is still 253.50 against 258.80 pegs, so the shutter jams at the top.

The leg is swept as a polygon in the (y,z) plane following its measured outer
edge, extruded across each wall strip.  Cylinders around all six dowel axes are
protected so no bore is opened any further than it already is.
"""
import trimesh, numpy as np
from shapely.geometry import Polygon
from _occ import L
MF='manifold'
T = np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]])
Tinv = np.linalg.inv(T)
# measured outer edge of the return leg
EDGE = [(238.5,136.5),(241.,136.0),(244.,136.5),(247.,137.0),(251.5,137.0),
        (254.5,136.5),(257.5,135.75),(260.5,134.5),(263.5,132.75),(266.5,130.5),
        (269.5,127.5),(272.5,123.25),(275.5,114.25),(276.5,110.5)]
THK = 10.0
STRIPS = {'left':(-131.62,-129.50), 'right':(124.00,128.40)}
BORES = [(-126,108),(-126,124),(0,108),(0,126),(126,104),(124,124)]
PROT_R, PROT_Z0, PROT_Z1 = 4.0, 238.0, 256.0

crown = L('CROWN_before_return.3mf'); crown.apply_transform(T)
V0, B0 = crown.volume, crown.bounds.copy()
n0 = len(crown.split(only_watertight=False))
print('crown in: %.3f cm3, %d bodies, wt %s' % (V0/1000,n0,crown.is_watertight))

poly = Polygon([(yh, z) for z,yh in EDGE] + [(yh-THK, z) for z,yh in reversed(EDGE)])
print('leg polygon area %.1f mm2' % poly.area)
R = np.array([[0.,0.,1.],[1.,0.,0.],[0.,1.,0.]])
cuts=[]
for nm,(x0,x1) in STRIPS.items():
    m = trimesh.creation.extrude_polygon(poly, height=x1-x0)
    M = np.eye(4); M[:3,:3]=R; M[:3,3]=[x0,0.,0.]
    m.apply_transform(M)
    b=m.bounds
    print('  %-5s cut x %8.2f..%8.2f  y %7.2f..%7.2f  z %7.2f..%7.2f  %.3f cm3'
          % (nm,b[0][0],b[1][0],b[0][1],b[1][1],b[0][2],b[1][2],m.volume/1000))
    cuts.append(m)
cut = trimesh.boolean.union(cuts, engine=MF)
prot=[]
for bx,by in BORES:
    c = trimesh.creation.cylinder(radius=PROT_R, height=PROT_Z1-PROT_Z0, sections=48)
    c.apply_translation([float(bx),float(by),(PROT_Z0+PROT_Z1)/2.])
    prot.append(c)
cut = trimesh.boolean.difference([cut]+prot, engine=MF)
print('cut after bore protection: %.3f cm3' % (cut.volume/1000))

out = trimesh.boolean.difference([crown, cut], engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out = trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(V0-out.volume)/1000
print('\ncrown out: %.3f cm3  removed %.3f  bodies %d  wt %s'
      % (out.volume/1000,dv,len(parts),out.is_watertight))
out.apply_transform(Tinv)
print('print bounds delta %s' % np.round(np.abs(out.bounds - L('CROWN_before_return.3mf').bounds),5).tolist())
assert out.is_watertight, 'crown not watertight'
assert len(parts)==n0, 'body count %d -> %d' % (n0,len(parts))
assert 0.5 < dv < 6.0, 'removed %.3f cm3' % dv
out.export('../VISAVERSE_v2/2_CROWN.3mf')
print('wrote 2_CROWN.3mf')
print('RFDONE')
