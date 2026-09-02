"""Exact inner edge of the retaining lip, base and crown, both sides.
Engagement = (rod tip) - (lip inner edge).  Lateral play = slot width - rod span.
"""
import trimesh, numpy as np
from _occ import L, Ts
D='../VISAVERSE_v2/'
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def has_roof(m,x,v):
    """is there material just above the slot roof at this x?"""
    ws=np.arange(145.8,148.4,0.05)
    P=np.column_stack([np.full(len(ws),x), np.full(len(ws),v), ws])
    return sol(m,P).mean() > 0.6
base=L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
crown=L(D+'2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
cs=crown.copy(); cs.apply_transform(Ts)
ROD_L, ROD_R = -130.980, 127.800
SLOT_L, SLOT_R = -131.60, 128.38
print('rod span %.3f .. %.3f (%.3f) ; slot %.2f .. %.2f (%.2f) ; lateral play %.2f'
      % (ROD_L,ROD_R,ROD_R-ROD_L,SLOT_L,SLOT_R,SLOT_R-SLOT_L,(SLOT_R-SLOT_L)-(ROD_R-ROD_L)))
for nm,m,v in (('BASE  v=100',bs,100.),('BASE  v=200',bs,200.),('CROWN v=225',cs,225.)):
    # left lip inner edge: walk inboard until the roof disappears
    L_edge=None
    for x in np.arange(-131.0,-118.0,0.1):
        if not has_roof(m,x,v): L_edge=x; break
    R_edge=None
    for x in np.arange(127.5,114.0,-0.1):
        if not has_roof(m,x,v): R_edge=x; break
    if L_edge is None or R_edge is None:
        print('  %-12s roof not found (L=%s R=%s)' % (nm,L_edge,R_edge)); continue
    print('  %-12s lip inner edges  L %8.2f  R %8.2f   ->  engagement  L %5.2f mm   R %5.2f mm'
          % (nm, L_edge, R_edge, L_edge-ROD_L, ROD_R-R_edge))
print('\nplate edges (lower panel): -123.220 / +117.320 - a lip may not reach past these')
print('LIPDONE')
