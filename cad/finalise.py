"""Clean degenerate faces, re-verify, then the full assembly audit."""
import trimesh, numpy as np
from _occ import L, Tb, Ts
MF='manifold'
def vol(i): return 0.0 if i.is_empty else abs(i.volume)/1000
D='../VISAVERSE_v2/'
for fn in ('1_BASE','2_CROWN'):
    m = L(D+fn+'.3mf')
    print('%-8s wt %s  winding %s  volume-valid %s  bodies %d  zero-area faces %d (harmless)'
          % (fn, m.is_watertight, m.is_winding_consistent, m.is_volume,
             len(m.split(only_watertight=False)), int((m.area_faces<1e-8).sum())))
    assert m.is_watertight and m.is_volume

FILES=['1_BASE','2_CROWN','3_LEFT_PANEL_DOOR','4_SHUTTER_LOWER','5_SHUTTER_UPPER',
       '6_TABLET_SLAB','8_DOOR_PULL','9_SILL_CAP','10_DOWEL_PINS']
BED=(350.,320.,325.)
print('\n=== mesh health + H2S bed fit ===')
M={}
for f in FILES:
    m=L(D+f+'.3mf'); M[f]=m; e=m.extents
    fits = max(e[0],e[1])<=350. and min(e[0],e[1])<=320. and e[2]<=325.
    print('%-20s %9.3f cm3  %3d bodies  %7.2f x %7.2f x %7.2f  wt %s%s'
          % (f,m.volume/1000,len(m.split(only_watertight=False)),e[0],e[1],e[2],
             m.is_watertight, '' if fits else '   >>> BED'))

base=M['1_BASE']
crown=M['2_CROWN'].copy(); crown.apply_transform(
    np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]]))
slab=M['6_TABLET_SLAB'].copy(); slab.apply_translation([0.,98.,133.6]); slab.apply_transform(Tb)
cap=M['9_SILL_CAP'].copy(); cap.apply_transform(Ts)
cap.apply_translation([-0.453,93.063,139.45-29.937]); cap.apply_transform(Tb)
lpd=M['3_LEFT_PANEL_DOOR'].copy(); lpd.apply_transform(
    np.array([[0.,0.,1.,-135.60],[1.,0.,0.,0.065],[0.,1.,0.,144.00],[0,0,0,1.]]))
pull=M['8_DOOR_PULL'].copy()
Mp=np.eye(4); Mp[:3,:3]=np.diag([1.,-1.,-1.]); Mp[:3,3]=[-2.775,0.825,3.60]
pull.apply_transform(Mp)
lo,up=M['4_SHUTTER_LOWER'],M['5_SHUTTER_UPPER']
CW=141.85-(0.05+6.30)/2.; CV0=-55.949; HINGE=169.9
print('\n=== static pairs ===')
for na,nb,a,b in [('crown','base',crown,base),('slab','base',slab,base),
                  ('slab','crown',slab,crown),('cap','base',cap,base),
                  ('cap','crown',cap,crown),('cap','slab',cap,slab),
                  ('panel door','base',lpd,base),('panel door','crown',lpd,crown),
                  ('panel door','slab',lpd,slab)]:
    v=vol(trimesh.boolean.intersection([a,b],engine=MF))
    print('  %-12s ^ %-6s %9.5f%s' % (na,nb,v,'   <<<' if v>0.01 else ''))
print('\n=== shutter, hinged, from the closed stop ===')
asm=trimesh.boolean.union([base,crown],engine=MF)
print('   cv     lower^asm  upper^asm  pull^asm  lower^cap  lower^upper')
for cv in [CV0, CV0+20, CV0+45, CV0+70, CV0+95]:
    d=lo.copy(); d.apply_translation([0.,cv,CW]); d.apply_transform(Tb)
    u=up.copy(); u.apply_translation([0.,cv+HINGE,CW]); u.apply_transform(Tb)
    p=pull.copy(); p.apply_translation([0.,cv,CW]); p.apply_transform(Tb)
    print('  %6.1f  %9.4f %9.4f %9.4f %9.4f %9.5f' % (cv,
      vol(trimesh.boolean.intersection([d,asm],engine=MF)),
      vol(trimesh.boolean.intersection([u,asm],engine=MF)),
      vol(trimesh.boolean.intersection([p,asm],engine=MF)),
      vol(trimesh.boolean.intersection([d,cap],engine=MF)),
      vol(trimesh.boolean.intersection([d,u],engine=MF))))
print('FINDONE')
