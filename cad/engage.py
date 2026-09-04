"""How far is the shutter's guide rod actually captured in the groove?

Engagement = (rod tip) - (groove shoulder).  Measure the groove profile in the
base and the crown, and the rod/plate extents on both panels.
"""
import trimesh, numpy as np
from _occ import L, Tb, Ts
D='../VISAVERSE_v2/'
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def edges(m,P,xs):
    s=sol(m,P); runs=[];st=None
    for i,v in enumerate(~s):
        if v and st is None: st=i
        if not v and st is not None: runs.append((xs[st],xs[i-1])); st=None
    if st is not None: runs.append((xs[st],xs[-1]))
    return runs

print('=== door cross-section (lower panel) ===')
lo=L(D+'4_SHUTTER_LOWER.3mf')
for z in (0.5, 2.0, 3.5, 5.0, 6.5):
    xs=np.arange(-135.,132.01,0.02)
    P=np.column_stack([xs, np.full(len(xs),100.0), np.full(len(xs),z)])
    s=sol(lo,P)
    if s.any():
        print('  z %4.1f : material x %8.3f .. %8.3f  (width %.3f)'
              % (z, xs[s].min(), xs[s].max(), xs[s].max()-xs[s].min()))
    else:
        print('  z %4.1f : none' % z)

print('\n=== base groove profile at v=100 (slope frame) ===')
base=L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
for w in (139.2, 140.5, 142.0, 143.5, 145.0, 145.6):
    us=np.arange(-136.,132.01,0.02)
    P=np.column_stack([us, np.full(len(us),100.0), np.full(len(us),w)])
    r=[q for q in edges(bs,P,us) if q[1]-q[0]>1.]
    print('  w %6.2f : void %s' % (w,'  '.join('%.2f..%.2f'%q for q in r) or 'none'))

print('\n=== crown groove profile (slope frame, v=225) ===')
crown=L(D+'2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
cs=crown.copy(); cs.apply_transform(Ts)
for w in (139.2, 140.5, 142.0, 143.5, 145.0, 145.6):
    us=np.arange(-136.,132.01,0.02)
    P=np.column_stack([us, np.full(len(us),225.0), np.full(len(us),w)])
    r=[q for q in edges(cs,P,us) if q[1]-q[0]>1.]
    print('  w %6.2f : void %s' % (w,'  '.join('%.2f..%.2f'%q for q in r) or 'none'))
print('ENGDONE')
