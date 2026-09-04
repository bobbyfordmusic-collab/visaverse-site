"""Can the shutter go in from the front, with the sill cap off?
Profile the base through the sill region at the door's own depth band, then
slide the lower panel forward and find what stops it."""
import trimesh, numpy as np
from _occ import L, Ts, Tb
MF='manifold'; D='../VISAVERSE_v2/'
def vol(i): return 0. if i.is_empty else abs(i.volume)/1000
base=L(D+'1_BASE.3mf'); bs=base.copy(); bs.apply_transform(Ts)
def sol(m,P):
    P=np.asarray(P,float); o=np.zeros(len(P),bool)
    for i in range(0,len(P),2000): o[i:i+2000]=m.contains(P[i:i+2000])
    return o
def runs(mask,ax):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: out.append((ax[s],ax[i-1])); s=None
    if s is not None: out.append((ax[s],ax[-1]))
    return out
print('=== base material along v through the sill, at the door depth band ===')
print('  (door occupies w 138.675..145.675; channel floor ~137.95)')
for u in (-100.,0.,100.):
    print(' u = %.0f' % u)
    for w in (138.70,139.20,139.80,140.50,142.00):
        vs=np.arange(-95.,-45.,0.05)
        P=np.column_stack([np.full(len(vs),u), vs, np.full(len(vs),w)])
        r=runs(sol(bs,P),vs)
        print('   w %6.2f : solid v %s' % (w,'  '.join('%.2f..%.2f'%q for q in r) or 'clear'))
print('\n=== slide the lower panel forward from the closed stop ===')
lo=L(D+'4_SHUTTER_LOWER.3mf'); CW=138.675
for cv in (-55.949,-58.,-62.,-70.,-80.,-100.,-140.,-190.):
    d=lo.copy(); d.apply_translation([0.,cv,CW]); d.apply_transform(Tb)
    i=trimesh.boolean.intersection([d,base],engine=MF)
    if i.is_empty:
        print('  cv %7.2f : clear'%cv); continue
    j=i.copy(); j.apply_transform(Ts); b=j.bounds
    print('  cv %7.2f : %8.4f cm3   u %7.2f..%7.2f  v %7.2f..%7.2f  w %7.3f..%7.3f'
          % (cv,vol(i),b[0][0],b[1][0],b[0][1],b[1][1],b[0][2],b[1][2]))
print('SILLDONE')
