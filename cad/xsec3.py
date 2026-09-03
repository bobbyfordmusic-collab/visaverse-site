"""Cross-sections of the crown in print orientation, via mesh slicing (cheap).
Find what carries the flange at print z 258.3 and how far it has to bridge."""
import trimesh, numpy as np
from _occ import L
c = L('../VISAVERSE_v2/2_CROWN.3mf')
print('print bounds', np.round(c.bounds,2).tolist())
print('\n   z      area mm2   n regions   region bboxes (x0,y0)-(x1,y1)')
for z in (200.,230.,245.,250.,254.,256.,257.,258.,258.6,260.,262.,265.,267.):
    try:
        s = c.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
        if s is None: print('  %6.1f   (empty)' % z); continue
        p,_ = s.to_planar()
        polys = p.polygons_full
        area = sum(q.area for q in polys)
        boxes = '  '.join('(%.1f,%.1f)-(%.1f,%.1f)'%(q.bounds[0],q.bounds[1],q.bounds[2],q.bounds[3])
                          for q in sorted(polys,key=lambda q:-q.area)[:3])
        print('  %6.1f   %8.1f   %5d      %s' % (z, area, len(polys), boxes))
    except Exception as e:
        print('  %6.1f   error %s' % (z, e))
print('XS3DONE')
