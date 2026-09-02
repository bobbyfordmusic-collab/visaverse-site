"""Where exactly did the straight cut breach the crown's roof?  Measure the
strip void beyond the channel roof, and the crown's outer surface radius."""
import trimesh, numpy as np
from _occ import L
CY, CZ = 110.12, 247.94
c = L('CROWN_before_apex.3mf'); c.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
c0 = L('CROWN_before.3mf'); c0.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
def sol(m,pts):
    pts=np.asarray(pts,float); o=np.zeros(len(pts),bool)
    for i in range(0,len(pts),3000): o[i:i+3000]=m.contains(pts[i:i+3000])
    return o
RR=np.arange(26.0,34.01,0.25); TH=np.arange(50.,131.,5.)
print('  theta |  NOW: solid r-band in strip |  ORIGINAL: solid r-band  | breach')
for lane,xs in (('left',[-131.0,-130.5,-130.0]),('right',[124.6,126.0,127.8])):
    print(' --- %s strip ---' % lane)
    for t in TH:
        P=[];  idx=[]
        for r in RR:
            y=CY+r*np.cos(np.radians(t)); z=CZ+r*np.sin(np.radians(t))
            for x in xs: P.append([x,y,z]); idx.append(r)
        sn=sol(c,P); so=sol(c0,P)
        dn={}; do={}
        for r,a,b in zip(idx,sn,so):
            dn[r]=dn.get(r,False) or a; do[r]=do.get(r,False) or b
        rn=[r for r in RR if dn[r]]; ro=[r for r in RR if do[r]]
        breach = len([r for r in RR if do[r] and not dn[r]])*0.25
        print('  %5.1f | %-27s | %-24s | %.2f mm'
              % (t, ('%.2f..%.2f'%(min(rn),max(rn))) if rn else 'none',
                    ('%.2f..%.2f'%(min(ro),max(ro))) if ro else 'none', breach))
print('RMDONE')
