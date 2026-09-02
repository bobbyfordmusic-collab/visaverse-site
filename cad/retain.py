"""What stops the shutter lifting out of its slot?
Scan w (through the slot's depth) at several x, in base and crown.  If the slot
is taller at the edges than in the middle, the middle roof is the retaining lip.
"""
import trimesh, numpy as np
from _occ import L, Ts
D='../VISAVERSE_v2/'
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def slot(m,x,v,w0=134.,w1=154.):
    ws=np.arange(w0,w1,0.02)
    P=np.column_stack([np.full(len(ws),x), np.full(len(ws),v), ws])
    s=~sol(m,P); runs=[];st=None
    for i,q in enumerate(s):
        if q and st is None: st=i
        if not q and st is not None: runs.append((ws[st],ws[i-1])); st=None
    if st is not None: runs.append((ws[st],ws[-1]))
    return [r for r in runs if r[1]-r[0]>0.5]
base=L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
crown=L(D+'2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
cs=crown.copy(); cs.apply_transform(Ts)
XS=(-130.0,-127.0,-124.0,-120.0,-100.0,0.,100.,120.,124.0,126.5,128.0)
for nm,m,v in (('BASE  v=100',bs,100.),('BASE  v=200',bs,200.),('CROWN v=225',cs,225.)):
    print('\n=== %s : slot extent in w at each x ===' % nm)
    for x in XS:
        r=slot(m,x,v)
        print('   x %8.1f : %s' % (x,'  '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in r) or 'none'))
print('RETDONE')
