"""How far does the flange overhang the shaft below it?
Take the flat ceiling faces at print z 258.30 and measure, for each, the
distance to the nearest solid material 1 mm below."""
import trimesh, numpy as np
from shapely.geometry import Polygon, MultiPolygon
from _occ import L
c = L('../VISAVERSE_v2/2_CROWN.3mf')
def outline(z):
    s = c.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
    p,T = s.to_planar()
    Ti = np.linalg.inv(T)
    polys=[]
    for q in p.polygons_full:
        pts=np.array(q.exterior.coords)
        P=np.column_stack([pts[:,0],pts[:,1],np.zeros(len(pts)),np.ones(len(pts))]) @ Ti.T
        polys.append(Polygon(P[:,:2]))
    return MultiPolygon(polys) if len(polys)>1 else polys[0]
below = outline(257.5)
above = outline(259.2)
print('area below z258 : %.1f mm2' % below.area)
print('area above z258 : %.1f mm2' % above.area)
new = above.difference(below)
print('newly appearing : %.1f mm2' % new.area)
# how far does the new material reach from the supported region?
try:
    parts = list(new.geoms)
except AttributeError:
    parts = [new]
print('\nunsupported patches (area, max reach from supported material):')
tot=0.
for g in sorted(parts, key=lambda q:-q.area):
    if g.area < 5: continue
    pts=np.array(g.exterior.coords)
    d=max(below.exterior.distance(__import__('shapely').geometry.Point(*p)) if below.geom_type=='Polygon'
          else min(q.exterior.distance(__import__('shapely').geometry.Point(*p)) for q in below.geoms)
          for p in pts)
    tot+=g.area
    print('   %8.1f mm2   max reach %5.2f mm   bbox %s'
          % (g.area, d, np.round(g.bounds,1).tolist()))
print('\ntotal unsupported %.1f mm2' % tot)
print('PROJDONE')
