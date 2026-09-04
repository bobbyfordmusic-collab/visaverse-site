"""Both shutter panels, correctly hinged 169.9 apart, swept together from the
closed stop.  The upper panel sits at cv+169.9 and was never covered by the
old -70..+83 sweep."""
import trimesh, numpy as np
from _occ import L, Tb, Ts
MF='manifold'
def vol(i): return 0.0 if i.is_empty else abs(i.volume)/1000
lo = L('../VISAVERSE_v2/4_SHUTTER_LOWER.3mf')
up = L('../VISAVERSE_v2/5_SHUTTER_UPPER.3mf')
pull0 = L('../VISAVERSE_v2/8_DOOR_PULL.3mf')
M=np.eye(4); M[:3,:3]=np.diag([1.,-1.,-1.]); M[:3,3]=[-2.775,0.825,3.60]
pull0.apply_transform(M)
base = L('../VISAVERSE_v2/1_BASE.3mf')
crown= L('../VISAVERSE_v2/2_CROWN.3mf'); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
cap  = L('../VISAVERSE_v2/9_SILL_CAP.3mf'); cap.apply_transform(Ts)
cap.apply_translation([-0.453,93.063,139.45-29.937]); cap.apply_transform(Tb)
asm = trimesh.boolean.union([base, crown], engine=MF)
CW = 141.85-(0.05+6.30)/2.; CV0=-55.949; HINGE=169.9

print('hinge check (lower at 0, upper at +%.1f): %.5f cm3'
      % (HINGE, vol(trimesh.boolean.intersection(
          [lo, up.copy().apply_translation([0.,HINGE,0.]) or up], engine=MF))))
u2 = up.copy(); u2.apply_translation([0.,HINGE,0.])
print('  recomputed: %.5f' % vol(trimesh.boolean.intersection([lo,u2],engine=MF)))
print('  lower v %.2f..%.2f   upper v %.2f..%.2f (hinged)'
      % (lo.bounds[0][1],lo.bounds[1][1],u2.bounds[0][1],u2.bounds[1][1]))

print('\n   cv     lower^asm  upper^asm  pull^asm  lower^cap  upper^cap')
worst=0.; wc=None
for cv in np.arange(CV0, CV0+140.1, 7.0):
    d=lo.copy(); d.apply_translation([0.,cv,CW]); d.apply_transform(Tb)
    u=up.copy(); u.apply_translation([0.,cv+HINGE,CW]); u.apply_transform(Tb)
    p=pull0.copy(); p.apply_translation([0.,cv,CW]); p.apply_transform(Tb)
    a=vol(trimesh.boolean.intersection([d,asm],engine=MF))
    b=vol(trimesh.boolean.intersection([u,asm],engine=MF))
    c=vol(trimesh.boolean.intersection([p,asm],engine=MF))
    e=vol(trimesh.boolean.intersection([d,cap],engine=MF))
    f=vol(trimesh.boolean.intersection([u,cap],engine=MF))
    m=max(a,b,c)
    if m>worst: worst,wc=m,cv
    print('  %6.1f  %9.4f %9.4f %9.4f %9.4f %9.4f' % (cv,a,b,c,e,f))
print('\nworst %.4f cm3 at cv %s' % (worst,wc))
print('SHUTDONE')
