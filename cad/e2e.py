"""One continuous scan of the whole door track, base and crown together, in a
single consistent set of stations: slope run -> crown arc -> stow slot.
At each station: clear x-span at three heights inside the rod band.  Rod ends
span 258.78, so anything under 258.80 is a fail.  Point containment only."""
import trimesh, numpy as np
from _occ import L, Tb
base=L('../VISAVERSE_v2/1_BASE.3mf')
crown=L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
def solid(P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),1500):
        q=P[i:i+1500]; o[i:i+1500]=base.contains(q)|crown.contains(q)
    return o
XL=np.arange(-135.,-124.99,0.05); XR=np.arange(122.,132.01,0.05)
def clear_at(pts_fn):
    """pts_fn(x) -> base-coord point.  returns (left wall, right wall, span)."""
    PL=np.array([pts_fn(x) for x in XL]); PR=np.array([pts_fn(x) for x in XR])
    sL=solid(PL); sR=solid(PR)
    # left wall = last solid x before the void; right wall = first solid after
    li=np.where(sL)[0]; ri=np.where(sR)[0]
    if not len(li) or not len(ri): return None
    lw=XL[li[-1]]; rw=XR[ri[0]]
    return lw,rw,rw-lw
stations=[]
# 1. slope run, slope frame, w at rod band (rod occupies ~w 140.2..144.2)
for v in np.arange(-60.,246.,6.):
    for w in (140.6,142.2,143.8):
        stations.append(('slope v=%.0f w=%.1f'%(v,w),
            lambda x,v=v,w=w: trimesh.transform_points([[x,v,w]],Tb)[0]))
# 2. crown arc, centre base (y 110.12, z 247.94), rod radii ~21..25
for t in np.arange(150.,29.,-6.):
    for r in (21.4,23.2,25.0):
        stations.append(('arc t=%.0f r=%.1f'%(t,r),
            lambda x,t=t,r=r: [x, 110.12+r*np.cos(np.radians(t)), 247.94+r*np.sin(np.radians(t))]))
# 3. stow slot, base frame: slot centre y = 123.625 + 0.1767*(z-60), rod band +-1.8 about it
for z in np.arange(236.,39.,-7.):
    yc=123.625+0.1767*(z-60.)
    for dy in (-1.8,0.,1.8):
        stations.append(('slot z=%.0f y=%.1f'%(z,yc+dy),
            lambda x,y=yc+dy,z=z: [x,y,z]))
worst=(1e9,None); fails=[]
print('%d stations' % len(stations))
for name,fn in stations:
    r=clear_at(fn)
    if r is None:
        fails.append((name,'no walls found')); continue
    lw,rw,sp=r
    if sp<worst[0]: worst=(sp,name)
    if sp<258.80: fails.append((name,'%.2f (walls %.2f / %.2f)'%(sp,lw,rw)))
print('narrowest clear span: %.2f mm at %s' % worst)
print('stations under 258.80: %d' % len(fails))
for f in fails[:40]: print('   ',f[0],':',f[1])
print('E2EDONE')
