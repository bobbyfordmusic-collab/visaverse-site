"""At the sill mouth, is there headroom above the lip for a slat to be lifted
over it and dropped into the channel?  The lip tops at w 139.939."""
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
def freew(u,v):
    ws=np.arange(136.,158.,0.05)
    P=np.column_stack([np.full(len(ws),u),np.full(len(ws),v),ws])
    s=sol(bs,P)|sol(cs,P)
    runs=[];st=None
    for i,q in enumerate(~s):
        if q and st is None: st=i
        if not q and st is not None: runs.append((ws[st],ws[i-1])); st=None
    if st is not None: runs.append((ws[st],ws[-1]))
    return [r for r in runs if r[1]-r[0]>0.4]
print('free depth (w) at the sill mouth and just inside it')
print('  lip top = 139.939 ; door is 8.80 thick (lower) / 7.00 (upper)')
print('   v      u=-120        u=-60         u=0           u=60          u=120')
for v in (-80.,-75.,-72.,-68.,-64.,-60.,-50.,-40.):
    cells=[]
    for u in (-120.,-60.,0.,60.,120.):
        f=freew(u,v)
        cells.append(('%.1f..%.1f'%f[0]) if f else 'none')
    print('  %5.0f   %-13s %-13s %-13s %-13s %s' % (v,*cells))
print('MOUTHDONE')
