"""Map the crown's curve as a field: where does a peg-width (>=258.80) opening
exist?  If the channel really carries the door round from the slope run into the
stow slot, those cells form one connected ribbon joining the two."""
import trimesh, numpy as np
from _occ import L
base = L('../VISAVERSE_v2/1_BASE.3mf')
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
RB=trimesh.ray.ray_triangle.RayMeshIntersector(base)
RC=trimesh.ray.ray_triangle.RayMeshIntersector(crown)
def widest(y,z):
    sol=[]
    for r in (RB,RC):
        loc,_,_=r.intersects_location(np.array([[-300.,y,z]]),np.array([[1.,0.,0.]]),multiple_hits=True)
        if not len(loc): continue
        xs=np.sort(np.round(loc[:,0],5)); xs=xs[np.concatenate([[True],np.diff(xs)>1e-4])]
        if len(xs)%2: xs=xs[:-1]
        sol+=[(xs[i],xs[i+1]) for i in range(0,len(xs),2)]
    sol=sorted(sol)
    if len(sol)<2: return 0.
    m=[list(sol[0])]
    for a,b in sol[1:]:
        if a<=m[-1][1]+1e-6: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    g=[m[i+1][0]-m[i][1] for i in range(len(m)-1)]
    g=[x for x in g if x>100.]
    return max(g) if g else 0.
YS=np.arange(70.,146.1,2.0); ZS=np.arange(230.,280.1,2.0)
grid=np.zeros((len(ZS),len(YS)))
for i,z in enumerate(ZS):
    for j,y in enumerate(YS):
        grid[i,j]=widest(y,z)
print('  peg-width map:  #  >=258.80    +  >=250    .  >=100    (blank) solid/none')
print('     y:  ' + ''.join('%d'%int((y//10)%10) for y in YS))
print('         ' + ''.join('%d'%int(y%10) for y in YS))
for i in range(len(ZS)-1,-1,-1):
    row=''
    for j in range(len(YS)):
        v=grid[i,j]
        row += '#' if v>=258.80 else ('+' if v>=250. else ('.' if v>=100. else ' '))
    print('  z%4d  %s' % (int(ZS[i]), row))
np.save('curvegrid.npy', grid)
print('CMDONE')
