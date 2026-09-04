"""Verify: pegs clear all the way round, and the roof is whole again."""
import trimesh, numpy as np
from _occ import L
CY, CZ = 110.12, 247.94
T = np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]])
c  = L('../VISAVERSE_v2/2_CROWN.3mf'); c.apply_transform(T)
c0 = L('CROWN_before.3mf'); c0.apply_transform(T)
print('crown: wt %s  winding %s  is_volume %s  bodies %d  vol %.3f cm3'
      % (c.is_watertight, c.is_winding_consistent, c.is_volume,
         len(c.split(only_watertight=False)), c.volume/1000))
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
LANES={'left':[-131.0,-130.5,-130.0],'right':[124.6,126.0,127.8]}
TH=np.arange(30.,151.,6.); RR=np.arange(18.,32.01,0.25)
print('\n  theta |  left strip void band   | right strip void band  | pegs 20.9..25.4')
bad=[]
for t in TH:
    row=[]
    for nm,xs in LANES.items():
        P=[];idx=[]
        for r in RR:
            y=CY+r*np.cos(np.radians(t)); z=CZ+r*np.sin(np.radians(t))
            for x in xs: P.append([x,y,z]); idx.append(r)
        s=sol(c,P); d={}
        for r,v in zip(idx,s): d[r]=d.get(r,True) and (not v)
        rs=[r for r in RR if d[r]]
        if not rs: row.append((None,None)); continue
        # contiguous band containing the peg zone
        lo=hi=None
        for r in rs:
            if 20.9<=r<=25.4: lo=r if lo is None else lo; hi=r
        row.append((min(rs),max(rs)))
    ok=[]
    for (lo,hi) in row:
        ok.append(lo is not None and lo<=20.9 and hi>=25.4)
    if not all(ok): bad.append(t)
    print('  %5.1f |  %-22s |  %-21s | %s'
          % (t, '%.2f..%.2f'%row[0] if row[0][0] is not None else 'none',
                '%.2f..%.2f'%row[1] if row[1][0] is not None else 'none',
                'OK' if all(ok) else '<<< STILL BLOCKED'))
print('\npeg path: %s' % ('CLEAR at every angle' if not bad else 'blocked at %s'%bad))
print('\nroof integrity in the strips (solid must reach the outer surface)')
print('  theta |  now solid band  | original solid band | breach')
for t in np.arange(50.,131.,10.):
    out=[]
    for nm,xs in LANES.items():
        P=[];idx=[]
        for r in np.arange(26.,34.01,0.25):
            y=CY+r*np.cos(np.radians(t)); z=CZ+r*np.sin(np.radians(t))
            for x in xs: P.append([x,y,z]); idx.append(r)
        sn=sol(c,P); so=sol(c0,P)
        dn={};do={}
        for r,a,b in zip(idx,sn,so): dn[r]=dn.get(r,False) or a; do[r]=do.get(r,False) or b
        rn=[r for r in np.arange(26.,34.01,0.25) if dn[r]]
        ro=[r for r in np.arange(26.,34.01,0.25) if do[r]]
        br=len([r for r in np.arange(26.,34.01,0.25) if do[r] and not dn[r]])*0.25
        out.append((('%.2f..%.2f'%(min(rn),max(rn))) if rn else 'none',
                    ('%.2f..%.2f'%(min(ro),max(ro))) if ro else 'none', br))
    print('  %5.1f | L %-15s %-15s %.2f | R %-15s %-15s %.2f'
          % (t,out[0][0],out[0][1],out[0][2],out[1][0],out[1][1],out[1][2]))
print('AVDONE')
