# Vis-A-Verse — printable parts

Master files are `.3mf`. Export STL from these; do not treat any STL as the source.

Printer: Bambu H2S, ASA.

## Files here

| file | volume | state |
|---|---|---|
| `1_BASE.3mf` | 4663.848 cm³ | current |
| `4_SHUTTER_LOWER.3mf` | 195.532 cm³ | current |
| `5_SHUTTER_UPPER.3mf` | 184.175 cm³ | current |
| `2_CROWN.3mf` | 222.773 cm³ | current |
| `6_TABLET_SLAB.3mf` | 935.543 cm³ | current, do not modify |
| `9_SILL_CAP.3mf` | 23.508 cm³ | current, do not modify |
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

A parking socket for the fan lead's USB-A male end, so it has somewhere to live
when unplugged. It is in the **ceiling of the interior cavity** — the underside
of the slab-pocket floor — 44 mm to the right of the fan, opening downward into
the cavity.

- slope `(u, v) = (42.0, 75.0)`, mouth at `w 93.00`; base coords `(42.0, -2.28, 119.45)`
- **12.6 x 5.1**, **13.48 mm deep**, with a 0.5 mm lead-in over the first 1 mm
- cut into 22.2 mm of solid, so ~8.8 mm of material remains above it

## Checks any base edit must still pass

- watertight, **43 bodies**, outer bounds unchanged to 1e-6
- all six dowel holes open **and still round** (6.30, or 6.40 at x=0)
- both shutter doors sweep their full travel at **0.0000 cm³** interference
- sill cap seats at ≤ 5e-4 cm³ (contact only, zero-thickness lumps)
- lower door hinge bore clear from the left edge to 121.95, blind stop intact
