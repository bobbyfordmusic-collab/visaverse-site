# Vis-A-Verse — printable parts

Master files are `.3mf`. Export STL from these; do not treat any STL as the source.

Printer: Bambu H2S, ASA.

## Files here

| file | volume | state |
|---|---|---|
| `1_BASE.3mf` | 4662.953 cm³ | current |
| `4_SHUTTER_LOWER.3mf` | 195.532 cm³ | current |
| `5_SHUTTER_UPPER.3mf` | 184.175 cm³ | current |
| `2_CROWN.3mf` | 223.411 cm³ | current |
| `6_TABLET_SLAB.3mf` | 935.543 cm³ | current, do not modify |
| `9_SILL_CAP.3mf` | 23.508 cm³ | current, do not modify |

Not yet in this folder — re-add when available: `3_LEFT_PANEL_DOOR`,
`7_FAN_CARTRIDGE`, `8_DOOR_PULL`.

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
same 4.48 / 3.90 mm of outer wall. The dowel bores at x 0 / ±126 sit forward of
the slot's y band and must not be touched when this is adjusted.

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

## Checks any base edit must still pass

- watertight, **43 bodies**, outer bounds unchanged to 1e-6
- all six dowel holes open
- both shutter doors sweep their full travel at **0.0000 cm³** interference
- sill cap seats at ≤ 5e-4 cm³ (contact only, zero-thickness lumps)
- lower door hinge bore clear from the left edge to 121.95, blind stop intact
