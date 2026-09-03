"""The deep-slot prism missed the slot's last 5 mm because the slot bends
toward lower y at its floor (y 104..120 at z 35..42, not the 119 the straight
centreline predicts).  Cut the two strips there with axis-aligned boxes over the
slot's actual band, down to the floor at z 34.5, so the rod ends stop on the
floor and not on a 2.6 mm step."""
import trimesh, numpy as np
from trimesh.creation import box as mk
from _occ import L
MF='manifold'
def bx(x0,x1,y0,y1,z0,z1):
    m=mk(extents=[x1-x0,y1-y0,z1-z0]); m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); return m
base=L('BASE_before_slotfloor.3mf'); V0=base.volume; B0=base.bounds.copy(); n0=len(base.split(only_watertight=False))
cuts=[bx(-131.62,-129.50,103.,121.,34.5,44.0), bx(124.00,128.40,103.,121.,34.5,44.0)]
out=trimesh.boolean.difference([base]+cuts,engine=MF)
parts=[p for p in out.split(only_watertight=False) if abs(p.volume)>1.0]
out=trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
dv=(V0-out.volume)/1000
print('base %.3f -> %.3f cm3 (removed %.4f)  bodies %d->%d  wt %s  vol %s  bounds moved %s'
      % (V0/1000,out.volume/1000,dv,n0,len(parts),out.is_watertight,out.is_volume,
         not np.allclose(out.bounds,B0,atol=1e-6)))
assert out.is_watertight and out.is_volume and len(parts)==n0 and np.allclose(out.bounds,B0,atol=1e-6) and 0<dv<1.0
out.export('../VISAVERSE_v2/1_BASE.3mf')
# verify with the door fitted, merged-solids ray method
lpd=L('../VISAVERSE_v2/3_LEFT_PANEL_DOOR.3mf'); lpd.apply_transform(
    np.array([[0.,0.,1.,-135.60],[1.,0.,0.,0.065],[0.,1.,0.,144.00],[0,0,0,1.]]))
RB=trimesh.ray.ray_triangle.RayMeshIntersector(out); RD=trimesh.ray.ray_triangle.RayMeshIntersector(lpd)
def solids(R,y,z):
    loc,_,_=R.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
    if not len(loc): return []
    xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
    if len(xs)%2: xs=xs[:-1]
    return [(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
def gaps(y,z):
    s=sorted(solids(RB,y,z)+solids(RD,y,z))
    if len(s)<2: return []
    m=[list(s[0])]
    for a,b in s[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return [(m[i][1],m[i+1][0]) for i in range(len(m)-1) if m[i+1][0]-m[i][1]>100.]
print('\nslot bottom, base + fitted door: widest walled span by z')
for z in (34.,36.,38.,40.,42.,44.,48.):
    best=(0.,None,None)
    for y in np.arange(95.,126.01,0.5):
        for a,b in gaps(y,z):
            if b-a>best[0]: best=(b-a,y,(a,b))
    print('  z %4.0f : %s' % (z,('%.2f at y %.1f (%.2f/%.2f)%s'%(best[0],best[1],*best[2],'' if best[0]>=258.8 else '  <<<')) if best[1] else 'none (below the floor)'))
print('SFDONE')
