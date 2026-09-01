# Vis-A-Verse — printable parts

Master files are `.3mf`. Export STL from these; do not treat any STL as the source.

Printer: Bambu H2S, ASA.

## Files here

| file | volume | state |
|---|---|---|
| `1_BASE.3mf` | 4666.858 cm³ | current |
| `4_SHUTTER_LOWER.3mf` | 195.532 cm³ | current |
| `5_SHUTTER_UPPER.3mf` | 184.175 cm³ | current |
| `9_SILL_CAP.3mf` | 23.508 cm³ | current, do not modify |

Not yet in this folder — re-add when available: `2_CROWN`, `3_LEFT_PANEL_DOOR`,
`6_TABLET_SLAB`, `7_FAN_CARTRIDGE`, `8_DOOR_PULL`.

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

Sill cap interface

- Seat plane **w = 139.45**, flat over the cap's whole footprint,
  `v` -73.05…-62.85, full width.
- The cap has a 2.25 mm pad under each end (left `u` -136.10…-122.20, right
  `u` 115.20…132.30, front 8.50 mm). Clearance pockets are cut to w 137.15.
- Seated at `du -0.453, dv 93.063, dw 109.513` the cap's top lands at 148.449,
  0.047 mm below the side-wall tops at 148.496.

## Checks any base edit must still pass

- watertight, **43 bodies**, outer bounds unchanged to 1e-6
- all six dowel holes open
- both shutter doors sweep their full travel at **0.0000 cm³** interference
- sill cap seats at ≤ 5e-4 cm³ (contact only, zero-thickness lumps)
- lower door hinge bore clear from the left edge to 121.95, blind stop intact
