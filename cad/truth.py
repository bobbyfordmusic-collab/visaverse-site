"""Ground truth by point containment, plus mesh health."""
import trimesh, numpy as np
from _occ import L
T = np.array([[0.,0.,-1.,132.30],[0.,1.,0.,99.30],[1.,0.,0.,259.5347],[0,0,0,1.]])
c = L('../VISAVERSE_v2/2_CROWN.3mf'); c.apply_transform(T)
print('watertight %s  winding %s  volume-valid %s  bodies %d'
      % (c.is_watertight, c.is_winding_consistent, c.is_volume,
         len(c.split(only_watertight=False))))
print('faces %d  duplicate faces %d  degenerate %d'
      % (len(c.faces),
         len(c.faces) - len(np.unique(np.sort(c.faces,axis=1),axis=0)),
         int((c.area_faces < 1e-8).sum())))
print('\nchannel width by point containment (solid = X, void = .)')
xs = np.arange(-135., 133.01, 0.25)
for y,z,lbl in ((130.,250.,'return leg'), (132.,244.,'return leg'),
                (126.,268.,'return leg upper'), (95.,262.,'slope leg'),
                (140.,200.,'base stow slot')):
    m = c if z > 239.3 else None
    if m is None: continue
    P = np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
    s = m.contains(P)
    runs=[]; st=None
    for i,v in enumerate(s):
        if not v and st is None: st=i
        if v and st is not None: runs.append((xs[st],xs[i-1])); st=None
    if st is not None: runs.append((xs[st],xs[-1]))
    big=[r for r in runs if r[1]-r[0]>100.]
    print('  %-18s y %5.1f z %5.1f  void %s'
          % (lbl,y,z, ' '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in big) or 'none'))
b = L('../VISAVERSE_v2/1_BASE.3mf')
print('\nbase: watertight %s  winding %s  volume-valid %s  bodies %d'
      % (b.is_watertight, b.is_winding_consistent, b.is_volume,
         len(b.split(only_watertight=False))))
for y,z,lbl in ((140.,200.,'stow slot mid'), (130.,120.,'stow slot low')):
    P = np.column_stack([xs, np.full(len(xs),y), np.full(len(xs),z)])
    s = b.contains(P)
    runs=[]; st=None
    for i,v in enumerate(s):
        if not v and st is None: st=i
        if v and st is not None: runs.append((xs[st],xs[i-1])); st=None
    if st is not None: runs.append((xs[st],xs[-1]))
    big=[r for r in runs if r[1]-r[0]>100.]
    print('  %-18s y %5.1f z %5.1f  void %s'
          % (lbl,y,z,' '.join('%.2f..%.2f (%.2f)'%(a,b,b-a) for a,b in big) or 'none'))
print('TRDONE')
