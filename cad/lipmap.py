"""Where along the run does the retaining lip exist, taking base and crown
together?  Any v where the lip is missing on either side is a place the shutter
can lift out of its track."""
import trimesh, numpy as np
from _occ import L, Ts
D='../VISAVERSE_v2/'
base=L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
crown=L(D+'2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
cs=crown.copy(); cs.apply_transform(Ts)
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def roof(x,v):
    ws=np.arange(145.8,148.4,0.06)
    P=np.column_stack([np.full(len(ws),x), np.full(len(ws),v), ws])
    return (sol(bs,P)|sol(cs,P)).mean() > 0.6
ROD_L, ROD_R = -130.980, 127.800
print('  v      lip inner L    lip inner R    engagement L / R')
bad=[]
for v in np.arange(-60., 250.1, 12.):
    Le=None
    for x in np.arange(-131.2,-118.0,0.2):
        if not roof(x,v): Le=x; break
    Re=None
    for x in np.arange(127.6,114.0,-0.2):
        if not roof(x,v): Re=x; break
    eL = (Le-ROD_L) if Le is not None else 99.
    eR = (ROD_R-Re) if Re is not None else 99.
    flag = '' if min(eL,eR) >= 2.0 else '   <<<'
    if min(eL,eR) < 2.0: bad.append((v,eL,eR))
    print('  %6.0f  %11s  %13s    %5.2f / %5.2f%s'
          % (v, '%.2f'%Le if Le is not None else 'none',
                '%.2f'%Re if Re is not None else 'none', eL, eR, flag))
print()
print('places the rod is held by less than 2 mm: %s'
      % (', '.join('v=%.0f (%.2f/%.2f)'%t for t in bad) if bad else 'none'))
print('LMDONE')
