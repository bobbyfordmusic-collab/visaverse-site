"""Which face of the lower shutter panel is the VISIBLE one?
The 'Vis-A-Verse' lettering marks it.  If the lettering and the door-pull
sockets are on the same face, that face is outward and my w-mapping is inverted;
if they are on opposite faces, the pull really is mounted facing the slab."""
import trimesh, numpy as np
from _occ import L
lo = L('../VISAVERSE_v2/4_SHUTTER_LOWER.3mf')
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
print('lower panel print bounds', np.round(lo.bounds,3).tolist())

# --- find the lettering: a band of fine detail. Scan both faces just inside
# the surface and count how broken up the material is along x.
for nm, zs in (('z=0 face (inner in my mapping)', [0.15, 0.35, 0.60]),
               ('z=8.8/7.0 face (outer)',        [2.35, 2.15, 1.90])):
    print('\n%s' % nm)
    for z in zs:
        best=None
        for y in np.arange(20., 160.1, 5.):
            xs=np.arange(-120.,120.01,0.4)
            P=np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
            m=sol(lo,P)
            # count transitions = how much fine detail sits at this height
            tr=int(np.sum(m[1:]!=m[:-1]))
            if best is None or tr>best[0]: best=(tr,y)
        print('   z %5.2f  max material transitions across x: %d (at y %.0f)'%(z,best[0],best[1]))

# --- where in z does the plate actually start/stop, at a plain spot
print('\nplate section at (x=0, y=60):')
zs=np.arange(0.,9.01,0.05)
P=np.column_stack([np.zeros(len(zs)), np.full(len(zs),60.), zs])
m=sol(lo,P); runs=[];s=None
for i,v in enumerate(m):
    if v and s is None: s=i
    if not v and s is not None: runs.append((zs[s],zs[i-1])); s=None
if s is not None: runs.append((zs[s],zs[-1]))
print('   solid z:', '  '.join('%.2f..%.2f'%r for r in runs))

# --- the pull sockets: which face do they open on?
print('\npull socket at (x=27.30, y=0.75):')
zs=np.arange(0.,9.01,0.05)
P=np.column_stack([np.full(len(zs),27.30), np.full(len(zs),0.75), zs])
m=sol(lo,P); runs=[];s=None
for i,v in enumerate(m):
    if v and s is None: s=i
    if not v and s is not None: runs.append((zs[s],zs[i-1])); s=None
if s is not None: runs.append((zs[s],zs[-1]))
print('   solid z:', '  '.join('%.2f..%.2f'%r for r in runs) or 'none (open right through)')
print('PFDONE')
