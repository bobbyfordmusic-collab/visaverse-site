"""The panel joint takes a cut piece of 1.75 mm filament - the user's method.
Remove the Ø2.10 x 250 rod I added; it is not needed.  Also check the magnet
alignment properly, since the two audits disagreed."""
import trimesh, numpy as np
from _occ import L, Ts
D='../VISAVERSE_v2/'
pins = L(D+'10_DOWEL_PINS.3mf')
parts = sorted(pins.split(only_watertight=False), key=lambda p:-abs(p.volume))
keep = [p for p in parts if p.extents[1] < 60.]      # the 28 mm dowels only
out = trimesh.util.concatenate(keep)
print('pins: %d bodies -> %d, %.3f -> %.3f cm3, extents %s'
      % (len(parts), len(keep), pins.volume/1000, out.volume/1000, np.round(out.extents,2).tolist()))
assert len(keep)==8 and abs(out.volume/1000 - 6.293) < 0.01
out.export(D+'10_DOWEL_PINS.3mf')

print('\n=== filament pin fit ===')
print('  panel-joint bore Ø2.220 ; 1.75 mm filament -> 0.47 mm diametral slack')

print('\n=== magnets: door pockets vs cap recesses (the two audits disagreed) ===')
lo = L(D+'4_SHUTTER_LOWER.3mf')
cap = L(D+'9_SILL_CAP.3mf'); cap.apply_transform(Ts)
cap.apply_translation([-0.453, 93.063, 139.45-29.937])
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
xs=np.arange(-90.,90.01,0.02)
P=np.column_stack([xs, np.full(len(xs),-6.0), np.full(len(xs),4.4)])
r=[q for q in runs(~sol(lo,P),xs) if q[1]-q[0]>2.]
print('  door pockets (x): %s' % '  '.join('%.2f..%.2f  c=%.2f  w=%.2f'%(a,b,(a+b)/2,b-a) for a,b in r))
us=np.arange(-90.,90.01,0.02)
P=np.column_stack([us, np.full(len(us),-64.0), np.full(len(us),143.5)])
r2=[q for q in runs(~sol(cap,P),us) if q[1]-q[0]>2.]
print('  cap recesses (u): %s' % '  '.join('%.2f..%.2f  c=%.2f  w=%.2f'%(a,b,(a+b)/2,b-a) for a,b in r2))
if r and r2:
    for (a,b),(c,d) in zip(r,r2):
        print('    centre offset %.2f mm' % abs((a+b)/2-(c+d)/2))
print('RODDONE')
