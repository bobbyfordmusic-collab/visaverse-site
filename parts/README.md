# Vis-A-Verse — printable parts

Master files are `.3mf`. Export STL from these; do not treat any STL as the source.

Printer: Bambu H2S, ASA.

## Files here

| file | volume | state |
|---|---|---|
| `1_BASE.3mf` | 4665.459 cm³ | current |
| `4_SHUTTER_LOWER.3mf` | 195.532 cm³ | current |
| `5_SHUTTER_UPPER.3mf` | 184.175 cm³ | current |
| `2_CROWN.3mf` | 222.773 cm³ | current |
| `6_TABLET_SLAB.3mf` | 935.543 cm³ | current, do not modify |
| `9_SILL_CAP.3mf` | 23.372 cm³ | current |
| `10_DOWEL_PINS.3mf` | 6.293 cm³ | 8 pins on one plate (5 needed) |
| `3_LEFT_PANEL_DOOR.3mf` | 100.324 cm³ | current, do not modify |
| `8_DOOR_PULL.3mf` | 6.891 cm³ | current |

`7_FAN_CARTRIDGE` is **retired** — the fan now mounts directly in the base, so
that part is no longer printed.

## Frozen — do not change

- **Left panel door fit.** Confirmed fitting on the printed base. The base's tab
  openings and the door's tab tops are final. Measured on the base, so the fit is
  recoverable even without the door file (base coords, left face):

  | | y | z | depth |
  |---|---|---|---|
  | door face plane | | | `x = -132.200` |
  | socket 1 | -96.00…-54.00 | 25.25…39.25 | 3.30 |
  | socket 2 | -21.00…+21.00 | 25.00…39.25 | 3.30 |
  | socket 3 | +49.00…+91.00 | 25.25…39.25 | 3.30 |

  Three sockets, 42.00 wide × 14.00 tall × 3.30 deep, centres at y -75 / 0 / +70.
  Three is the count — do not add or remove one.
- **Front D-handle.** Final.
- **Sill cap.** Final. The base is cut to suit the cap, never the reverse.
- **Dowel holes.** On the absolute top face of the base, `z = 239.2747`, at
  `(x, y)` = (-126,108) (-126,124) (0,108) (0,126) (126,104) (124,124).
  Any base edit must leave the outer bounds unchanged to the micron.
- **Shutter guide peg length.** Door edges at `u = -131.00` / `+127.80`
  (256.65 mm as printed and approved on the left). Widen the base, never shorten
  the pegs.

## Slope frame

Most base features are measured in a frame aligned to the sloped face:

```
W = normalize(0, -0.6425, 0.7663)
U = (1, 0, 0)
V = W × U
R = column_stack([U, V, W])      base→slope uses Rᵀ, slope→base uses R
```

Coordinates below are `(u, v, w)` in that frame.

## Key dimensions

Shutter channel

| | left | right |
|---|---|---|
| groove back | -131.62 | +128.40 |
| groove face | -125.86 | +124.74 |
| groove floor | w 137.90 | w 138.02 |
| wall behind the groove | 4.48 mm | 3.90 mm |

The right wall is only 3.90 mm thick, so that side cannot be widened — lengthen
the peg there instead. The channel runs clear through the sill on both sides.

**Stowing slot** (top of the base, where the door parks when open). Its side
walls must match the channel: `x = -131.62 / +128.40`, **260.02** clear, against
a 258.80 door. It was 253.50 (-129.50 / +124.00) and jammed the door. Leaves the
same 4.48 / 3.90 mm of outer wall.

**The slot cut must be clamped to `y >= 128`.** The dowel bores at (-126,124) and
(124,124) span y 120.85…127.15, and an unclamped cut reaches them and turns those
two bores into open-sided slots (they measured 8.75 and 7.50 wide instead of
6.30). The slot's full-width band does not start until y ~130, so nothing is
lost by the clamp. After any slot edit, re-measure **all six** bores, not just
the four at y 104/108/126.

Sill cap interface

- Seat plane **w = 139.45**, flat over the cap's whole footprint,
  `v` -73.05…-62.85, full width.
- The cap has a 2.25 mm pad under each end (left `u` -136.10…-122.20, right
  `u` 115.20…132.30, front 8.50 mm). Clearance pockets are cut to w 137.15.
- Seated at `du -0.453, dv 93.063, dw 109.513` the cap's top lands at 148.449,
  0.047 mm below the side-wall tops at 148.496.

## Crown

The crown ships in print orientation. Its assembly transform onto the base is

```
base(x, y, z) = (132.30 - z_print,  y_print + 99.30,  x_print + 259.5347)
```

which lands its mating face on the base's top at `z = 239.2747` and its five
dowel bores exactly on the base's dowels at (-126,108) (-126,124) (0,108)
(124,124) (126,104). Keep that transform when checking anything against the base.

- **Door channel**: walls at `-131.62 / +128.40`, **260.02** clear, over the
  groove band `w 138.03…145.67`. Was -129.50 / +124.75 = 254.25 against a 258.80
  door, and the right side had no groove at all — the same fault the base had.
  The widening runs `v 190…280`, so assembled the channel is one uninterrupted
  260.02 from `v 150` deep in the base, through the base/crown joint at `v ≈ 204`,
  out to `v 252`. The base's stowing slot starts at `v ≈ 245` (slope
  `w 65…105`), so the full-width channel covers the hand-off. Past `v 258` the
  crown's own top structure closes in, by which point the door has turned down
  into the slot.
- **The channel never shares space with the slab.** The groove sits at
  `u -131.62…-125.86` and `+124.74…+128.40`; the slab spans `±122.625`. Gap
  3.235 mm left, 2.115 mm right — a pure `u` comparison, independent of any
  assumption about the slab's height or depth.
- **Slab clearance**: the crown is glued on permanently and the slab is fitted
  and removed with it in place, so the crown is relieved over the whole motion,
  not just the seated pose. The motion is: the slab's top slides in under the
  crown, then the bottom drops into the sill; removal is the reverse. Modelled as
  a rotation about a u-axis at the slab's top edge (`PIV = 0, 251.0, 128.9` in
  slope coords, negative theta lifting the bottom out) combined with travel down
  the slope. The swept slab over `theta 0…-12°, dv 0…-20`, grown 0.40 mm along
  the slope normal, is subtracted. Seated pose is `dv 98.0, dw 133.6` via `Tb`.
- A thin cross rail at `v 229…231, w 135.0…137.2` sat inside the slab's handle
  recess and was freed by that cut; it is gone deliberately.

Crown checks: watertight, **one body**, print bounds unchanged, `crown ∩ base` =
0.00000, and the slab's full install/remove path clear at every step —
`theta` 0/-4/-8/-12 crossed with `dv` 0/-10/-20/-45 all read 0.0000 cm³.
The base never blocks that motion; only the crown did (17.87 cm³ before).

## Dowel pins

Crown-to-base locating pins, `10_DOWEL_PINS.3mf` — 8 on a plate, 5 are needed.

- **6.00 dia x 28.0 long**, 0.5 x 45° chamfer each end, printed standing.
- Bores: base **6.30** dia (6.40 at x=0), blind, floor `z 224.30`, depth 14.97.
  Crown **6.36** dia, depth 15.00. Pin gives 0.15 mm radial clearance in the
  tightest base bore, 0.18 in the crown.
- 28.0 against 14.97 + 15.00 = 29.97 of hole, so ~1 mm spare at each end — the
  pin can never hold the crown off the base.
- Five positions have a bore in **both** parts: (-126,108) (-126,124) (0,108)
  (124,124) (126,104). The base's sixth bore at **(0,126) has no crown mate** —
  leave it empty.
- Verified: pin seated on the bore floor reads ≤ 0.00088 cm³ against the base and
  0.00000 against the crown at all five positions, with 14.97 mm of engagement
  below the joint and 13.03 above.

## Fan mount

The fan mounts straight into the base; there is no cartridge. Fan is a 5010 —
50 x 50 x 10 mm, 40 mm bolt pattern, Ø4.5 holes — and it **blows toward the slab,
drawing from the interior cavity**.

Cavity, in slope coords, fan centre `(u, v) = (-2.0, 75.0)`:

| w | feature |
|---|---|
| 93.0 … 97.4 | 56 x 60 mouth (was the cartridge rebate, now just a lead-in) |
| 97.4 … 107.42 | **51.0 x 51.0 pocket, 10.02 deep** — the fan drops in here from the cavity |
| 107.42 | **the ledge** the fan bottoms on |
| 107.42 … 115.25 | 46 x 46 throat, air passes through toward the slab |

The ledge already existed. What was missing was anything to screw into: the fan's
bolt holes sit ±20 mm from its centre, which is inside the 46 mm throat, so there
was no material there at all. Four **10 x 10 pads** are added in the throat
corners at the bolt positions, rising 6.58 mm off the ledge, each with a **Ø3.4
pilot 6.16 mm deep** for an M4 self-tapper. Bolt positions in slope coords:
(-22,55) (-22,95) (18,55) (18,95); in base coords (-22,-26.87,117.65)
(-22,3.78,143.35) (18,-26.87,117.65) (18,3.78,143.35).

Verified: a 50 x 50 x 10 block seated on the ledge reads 0.00857 cm³ against the
base (corner film only — real fan frames are radiused), all four pilots probe at
exactly 3.40 wide and blind.

## USB park

A parking socket for the fan lead's USB-A male end. It sits on the **cavity floor,
back right** (base coords), so the slack lies on the floor instead of hanging
across the cavity.

- centre `(x, y) = (100.0, 95.0)`, opening **12.6 x 5.1**, **13.0 mm deep**
- the floor there is only 7.95 mm thick (solid `z 38.55...46.50`) and the thicker
  rib further back is just 4.15 mm wide in y, so neither takes a sunk socket.
  The socket is instead sunk 5.0 mm into the floor with an 8.0 mm collar above:
  socket floor `z 41.50`, collar top `z 54.50`, leaving 2.98 mm of floor beneath
- 18 x 11 collar, so 2.7 mm wall in x and 2.95 in y; 0.5 mm lead-in over the top 1 mm
- verified: a 12.0 x 4.5 x 12 USB-A shell inserts at **0.00000 cm3**

## Door pull

The pull inserts into the lower shutter door. Its transform into the door's own
frame is a flip about x plus a translation:

```
M = diag(1, -1, -1),  t = (-2.775, 0.825, 3.60)
```

- two built-in pegs, **Ø6.75 x 3.4 long**, at door x **-32.70 / +27.30**, y 0.75
- they drop into sockets in the door's `z = 0` face, 6.60 x 6.80, **7.10 deep** —
  so 3.4 mm of peg in a 7.1 mm socket
- the pull's body then hangs below the door's outer face, door z -9.90 … 0
- verified: **pull ∩ lower door = 0.00000 cm³**, and 0.0000 against base+crown
  at every point of the door's travel

Separately, the door meets the cap by magnets, not by the pull: the door carries
pockets 10.00 x 6.00 x 2.15 at x ±55 on its `y = -7` edge, and the cap has
matching recesses 10.2 x 6.4 x 2.58 at u ±54.85 on its `+v` face.

## Sill cap — placement, and the door's closed stop

`dv = 93.063` (the cap's M3 at u 127.000 paired with the base's counterbore at
u 126.547). This is correct and is confirmed by the magnets, not just the screws.

The lower shutter door does not slide *over* the cap — its bottom edge **bumps
into** the cap, and that contact is what closes the shutter and brings the two
magnet pairs together.

- cap's facing surface (max v over the door's w band): **v -62.949**
- door's bottom edge: its own `y = -7`, so contact at **cv = -55.949**
- door magnet pockets 10.00 x 6.00 x 2.15 deep, centred x ±55.00, opening on the
  `y=-7` edge
- cap magnet recesses 10.03 x 6.4 x 2.58 deep, centred u -55.17 / +54.26 seated
  (±54.715 in the cap's own frame), opening on the v -62.949 face
- pocket pair meets face to face, 4.73 mm of combined depth for the magnet stack

At `cv = -55.949` the door reads 0.0029 cm³ against the cap (the contact plane
itself) and **0.0000 against the base, the crown and the door pull**. The whole
travel from that stop up to fully stowed is 0.0000 everywhere.

Any interference figure quoted for `cv` below -55.949 is meaningless — it is the
door driven past its physical stop, into the cap. An earlier note here claimed a
12.19 cm³ door/cap clash and a candidate cap position ~8 mm further forward; both
came from sweeping the door past the stop. There is no such clash.

## Known model-vs-print discrepancy

With the slab seated at `dv 98.0, dw 133.6` the slab's top face reads w 139.49
while the closed door's underside reads w 138.675 — the door plane passes
**0.802 mm** below the slab top, so the model shows a uniform 0.80 mm film of
overlap (2.74 cm³ lower, 2.45 cm³ upper) spread flat across the slab's whole top,
with no lump anywhere. The printed parts do not catch, so the model's slab seat
is ~0.8 mm shallower than the real one. Nothing has been cut for this; it is
recorded so the number is not re-derived as a fault.

## The door track — full path, verified (pre-print audit)

The shutter's guide pegs are **discrete**: 3 mm long, every 10 mm, on both edges
— 16 pairs on the lower panel, 17 on the upper. They run the whole length of
both panels, so they must follow the track everywhere, including down into the
stow slot.

Door cross-section (w = door z + 138.675):

| band | width |
|---|---|
| 138.675 – 140.42  body underside | 253.20 |
| 140.42  – 143.92  **guide pegs** | **258.80** |
| 143.92  – 144.92 | 249.50 |
| 144.92  – 147.48  raised back | 240.57 |

Only the 3.5 mm peg band needs 258.80; above and below, the door is far
narrower. A clearance check that demands peg width across the door's whole
thickness will report false failures — the crown's channel roof is legitimately
250.75 there.

**The track must be 260.02 wide over its entire length.** Two stretches were
still at the original 253.50 and were cut on this pass:

- **base, stow slot, z 36 – 176** — the slot runs z 36 → 236 and only its top
  58 mm had been widened. The door would have entered and jammed 58 mm down.
  Cut as a 10.02 deg tilted prism (centre plane `N.(y,z) = 111.28`,
  `N = (0, 0.9848, -0.1740)`, along `D = (0, 0.1740, 0.9848)`), 12.603 cm3.
- **crown, return leg, z 239 – 275** — the leg that hands the door back down
  into the stow slot. Its slope leg was already 260.02; the return leg was not.
  Cut as a swept polygon following the leg's measured outer edge, with r 4.0
  protection cylinders on all six dowel axes, 2.253 cm3.

Verified after: 260.02 continuous from the bottom of the slot (z 47) to the top
of the crown, confirmed by point containment on both legs; all six base dowel
bores still round at 6.40; no crown bore opened any further than it already was.

Walls left outside the track are 4.48 mm left / 3.90 mm right everywhere —
the same as the stretch that already prints.

## What the rigid model cannot check

The shutter is segmented (49 / 51 bodies) and bends round the crown. A rigid
translation of the panels reads ~6.9 cm3 into the crown at every position; that
figure is fixed at slope v 252.6..269.0 and does not move with the door, i.e. it
is the flat plate ploughing through the curve, not a collision. Below the curve
every position reads 0.0000. The curve is instead verified by track width, which
now holds 260.02 all the way round.

The two panels are hinged **169.9 mm apart** (lower at cv, upper at cv + 169.9);
at that offset they read 0.00000 against each other. Checking both at the same
cv is meaningless.

## Six-way cross-check audit — findings and fixes

An independent six-agent audit was run against this exact file set. What it
found, and what was done.

### Fixed

**Crown apex — the peg grooves missed the pegs entirely.** The crown's track is
a clean circular arc (outer wall R 26.715 about base y 110.428 / z 249.078, rms
residual 0.027 mm, turning 130.0 deg) but the groove had been cut on a straight
tangent. It drifted outward, so over theta 60..102 deg the pegs met solid — worst
4.10 mm at theta 84 — and at theta 85..95 the cut exited through the roof,
severing the crown's visible top surface completely. Fixed by restoring the roof
from the original crown (r >= 27.9, union, +0.293 cm3) then re-cutting the groove
along the true arc (r 19.5..27.5, theta 40..120, -0.444 cm3). Verified by point
containment: pegs clear at every angle 30..150, roof solid 28.00..31.75.

**Base seam — a 0.07 mm skin capped the groove at the crown joint.** The
stow-slot void stopped at z 239.20 against a top face at z 239.27, blocking the
groove at the exact hand-off. Cut through (0.0124 cm3).

**Sill cap — an unprintable 0.20 mm sliver tab.** The earlier pad trim left
0.20 mm of tab on the right (u 123.05..123.25 seated) against 6.35 mm on the
left. Removed (0.0048 cm3, bounds unchanged).

**Panel hinge rod added.** See below.

### Verified good — the one that could have killed the design

The shutter's slat joint is a concentric pin-in-closed-bore knuckle hinge: pin
Ø3.0921 in bore Ø4.0936, 0.5008 mm radial clearance, 10.000 mm pitch, 17 slats
per panel. It articulates to **91.65 deg per joint** (3D boolean: 0.0000 mm3 at
91 deg, 1.9867 mm3 at 92 deg), minimum bend radius 6.25 mm. The crown's curve
demands **26.03 deg per joint** at a pin-circle radius of 21.95 mm.
**Margin 3.52x.** The shutter bends far tighter than the crown asks. The slats
also cannot pull apart — the bore is a closed circle, and +2.0 mm of tension
gives 471 mm3 of interpenetration.

### Open — needs a decision, not a cut

- **The two panels have no hinge pin.** The panel joint at door y 170.000,
  z 3.500 is properly interdigitated (7 lower knuckles + 6 upper, 244 of 258.8 mm
  covered) and bored Ø2.220, but nothing in the file set fits it. A Ø2.10 x 250
  printable rod has been added to `10_DOWEL_PINS.3mf` as a stopgap; **a 2 mm
  steel rod 250 mm long is the better part.** Without it the shutter is two
  loose halves.
- **The door pull is on the inner face.** Sockets open on the panel's z = 0
  face; the lettering (0.610 mm deep, z 6.390..7.000) is on the z = 7 face, and
  w increases outward, so z = 7 is the visible side. The pull therefore points
  into the display aperture where no finger reaches. It also rattles: peg
  Ø4.980 in a 6.880 x 6.860 x 7.120 socket = 1.90 mm of slop. Not changed —
  moving it alters a part already printed and in use.
- **Shutter is permanent once the crown is glued.** Withdrawing a panel through
  the sill mouth is blocked by 1,299..1,545 mm3 of base at slope v -78.77..-72.32
  (a 1.26 mm raised sill floor) across nearly the full width; the crown is never
  the obstruction. **Panels must be fed in from the rear/stow end before the
  crown goes on**, and cannot be serviced afterwards.
- **Only 2 of 6 crown dowel bores are true closed bores** ((-126,124) and
  (124,124)). (0,108) has no crown bore at all and a pin there drives 10.63 mm
  into the slab — **do not fit a pin at (0,108)**. (0,126), (126,104) and
  (-126,108) are partial. Pre-existing in the supplied crown.
- **Slab seat.** The model's seated slab rests on a ~1 mm wide ramp crest at
  u 119.8..121.0, v 210..231 rather than on the pocket floor, which measures
  w 117.10 + 0.00271*v. Dropped onto the real floor the slab sits 0.7..1.6 mm
  lower and the door clears it — which is what the printed parts do. Not
  touched: the base pocket is frozen by instruction.
- **Slot taper, z 174..184.** The slot narrows 9.39 -> 7.81 mm perpendicular
  then steps back to 9.39. Against a 7.00 mm door that is 0.81 mm of clearance,
  not an interference. An attempt to open it removed 5.8 cm3 from the 3.2 mm rib
  behind the slot without widening the slot, and was reverted.
- **Magnet pockets** measure 20.240 x 6.240 x 2.150 centred x = +-60.000, not
  10 x 6 at +-55; the cap recesses are 20.6 x 6.55 x 2.62 at u -60.48 / +59.53.
  Glue the magnets to the outboard end of each slot. Stack depth 4.77 mm — use
  2 mm magnets.
- **Lettering** is chopped by the barrel crowns into three 3.95 mm stripes,
  losing ~60% of each glyph. It does not weaken the panel.

### Slicing notes (not model changes)

- **Rotate the base 90 deg on the plate.** As modelled, 310.26 mm on the 320 mm
  axis leaves 4.87 mm a side — no room for a brim. Rotated: 19.9 / 25.8 mm.
- Slab fits the 350 mm axis only (14.5 mm a side). Sill cap needs rotating onto
  its flat top face; the door pull prints bar-down.
- Keep the support threshold at or below 35 deg, or trees grow inside the stow
  slot and the sloped cavity where they cannot be removed.
- The 42 sealed voids in the foot are the rib plinths, on a 30 mm grid, 5.00 mm
  minimum wall — deliberate, not debris.
- The 66 small bodies on the shutter panels are the sacrificial snap-off pads
  under each rod end (0.31 mm gap). Deliberate — do not delete them.

## Audit follow-up — second pass

**Fixed this pass**

- Base **left sill pilot moved 0.800 mm** (u -130.800 -> -130.000). The sill cap
  seats at **u = 0**, proved three ways: the cap's x extents equal the base's
  exactly, its magnet recesses then coincide with the shutter's pockets to
  0.00 mm, and its right M3 hole already landed dead on the base pilot at
  u +127.000. Only the left pilot was out. Both now match.
- **0.22 mm floating membrane removed** from the panel-door opening
  (x -132.19..-131.97, y 107..117, z 31..43). Attached to nothing, below one
  extrusion width. Pre-existing, not introduced by the track work.
- **Cavity floor wedge closed** (+0.5054 cm3). A hairline void ran the full
  244 mm width at z 40.97..43.66, opening from 0.075 mm at y 101 to 0.815 at
  y 105, splitting the 8.03 mm floor into two ~4 mm slabs.
- **Hinge rod removed** from 10_DOWEL_PINS. The panel-to-panel joint takes a cut
  length of **1.75 mm filament** through the overlapping knuckles (Ø2.220 bore,
  0.47 mm slack) - the intended assembly method.

**Corrected audit findings that were wrong**

- Magnet pockets are **not** 5 mm out of position. Door pockets centre on
  x +-60.000, cap recesses on u -60.45 / +59.55; that 0.45 mm is exactly the
  cap's misplacement, and at u = 0 they coincide. The "expected +-55" they were
  judged against was my own bad number.
- The slot "pinch" at z 174..184 measures **7.81 mm** perpendicular, not 6.91 -
  0.81 mm of clearance against a 7.00 mm door, not an interference.
- The reported "slab 0.815 mm proud" is a seating artefact: the model's slab
  rests on a ~1 mm ramp crest rather than the pocket floor.

**Deliberately NOT cut, and why**

The three dowel-bore complaints are real but not worth the risk:

- **(0,126)** loses its rear wall above z ~231 (2.60 mm at z 228 -> 0.90 at
  z 230 -> 0 at z 232). Adding a wall means putting material into the stow
  slot's mouth, which is exactly where the door has to pass.
- **(-126,124)** and **(124,124)** rear walls taper 1.477 (z 234) -> 0.776
  (z 236) -> 0.008 mm (z 239) and print open at the very top face.
- **(-126,108)** is pinched 1.00 mm out of round at its floor; full-diameter
  depth is 13.78 mm rather than 14.97.

All six bores still measure a round 6.40 at z 228/232/236, and the crown joint
is located by the two sound crown bores at (-126,124) and (124,124), 250 mm
apart, plus glue. **Do not fit a pin at (0,108)** - the crown has no bore there
and a pin drives 10.63 mm into the slab's space.

## Checks any base edit must still pass

- watertight, **43 bodies**, outer bounds unchanged to 1e-6
- the stow slot holds **260.02 mm** from z 47 to z 236, and the crown
  carries 260.02 round both legs — check by point containment, not by
  ray casting (coplanar boolean faces make a ray scanner report false narrows)
- all six dowel holes open **and still round** (6.30, or 6.40 at x=0)
- both shutter doors sweep their full travel at **0.0000 cm³** interference
- sill cap seats at ≤ 5e-4 cm³ (contact only, zero-thickness lumps)
- lower door hinge bore clear from the left edge to 121.95, blind stop intact
