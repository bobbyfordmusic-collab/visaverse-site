"""Cap M3 holes vs base pilots - measure both myself; the audits disagreed."""
import trimesh, numpy as np
from _occ import L, Ts
D='../VISAVERSE_v2/'
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),3000): o[i:i+3000]=m.contains(P[i:i+3000])
    return o
def runs(mask,ax):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: out.append((ax[s],ax[i-1])); s=None
    if s is not None: out.append((ax[s],ax[-1]))
    return out
cap = L(D+'9_SILL_CAP.3mf'); cap.apply_transform(Ts)   # OWN frame (no shift)
b=cap.bounds; print('cap own-frame bounds', np.round(b,3).tolist())
print('\ncap through-holes, scanned in u at several w:')
for w in (31.0, 33.0, 35.0):
    us=np.arange(-136.,132.01,0.02)
    P=np.column_stack([us, np.full(len(us),-161.5), np.full(len(us),w)])
    r=[q for q in runs(~sol(cap,P),us) if 1.5<q[1]-q[0]<6.]
    print('  w %5.1f : %s' % (w,'  '.join('c=%.3f d=%.2f'%((a+b_)/2,b_-a) for a,b_ in r) or 'none'))
base = L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
print('\nbase sill pilots, scanned in u on the sill bar:')
for w in (138.0, 136.0, 134.0):
    for v in (-68.2, -68.31, -67.9):
        us=np.arange(-136.,132.01,0.02)
        P=np.column_stack([us, np.full(len(us),v), np.full(len(us),w)])
        r=[q for q in runs(~sol(bs,P),us) if 1.5<q[1]-q[0]<6.]
        if r: print('  w %5.1f v %7.2f : %s' % (w,v,'  '.join('c=%.3f d=%.2f'%((a+b_)/2,b_-a) for a,b_ in r)))
print('H3DONE')
