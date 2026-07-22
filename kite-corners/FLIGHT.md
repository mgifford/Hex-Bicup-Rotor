# Flying the Tetrahedral Kite

Practical flight information for a kite built from `kite_corner.scad`,
`kite_corner_interior.scad`, and `kite_corner_triple.scad` — where to
attach the line, how strong it needs to be, how heavy the kite can be and
still fly, and what wind and launch conditions to expect.

**This is a separate hobby side-project, not part of the VINDSNURR wind
rotor** — see [README.md](README.md) for that scope note and the
structural/assembly documentation this page builds on.

Everything below uses a **4-layer, 20-cell kite with 500mm struts (2m
base width)** as the worked example, matching the exploded-view diagram in
[README.md](README.md). The underlying math is shown so you can rescale it
for a different size or strut length — treat the specific numbers as
estimates to size your build, not guarantees, and verify against your
actual printed/assembled weight before a first flight.

---

## Where to attach the flight line

**Attach to one of Layer 0's 3 base-corner exterior hubs — never the top
apex.** These are the 3 vertices marked in red at the very bottom of the
exploded-view and front-view diagrams in [README.md](README.md). Pick the
one at a corner cell whose 2 outward-facing side faces are both covered
with sail — every reference build (Instructables, Kono-Bell) attaches at a
front-bottom corner, not the tip, and for the same structural reason: an
exterior hub is the lowest-stress joint (3 sockets only), so a line tied
there loads it in pure tension along already-loaded strut axes rather than
putting a bending moment sideways into a hub.

Tie the line (or loop it through a small eyelet you print or drill into
that hub) directly to the hub, not to a strut. Balance-test by hand in
light wind before committing to a long line.

---

## Weight budget — this is the part that actually determines whether it flies

**Key finding: the printed hubs are not the main weight problem — the
struts are.** At "1-2 meter" scale with 6mm rod (the default parameter
preset), this design comes out too heavy for reliable flight. Fixing it
means changing strut material and the matching hub size, not redesigning
the joints.

### The default (6mm rod) preset is too heavy above ~1m

Using the standard kite wing-loading measure (total weight ÷ sail area),
and real numbers — hub volumes computed directly from the exported STL
meshes (not estimated), sail area from the actual 20-cell geometry, typical
material weights for struts and ripstop nylon sail:

| Strut length | Base width | Sail area | Total weight (6mm rod) | Wing loading |
|---|---|---|---|---|
| 375mm | 1.5m | 1.95 m² | ~1225g | **629 g/m²** |
| 500mm | 2.0m | 3.46 m² | ~1595g | **460 g/m²** |
| 750mm | 3.0m | 7.79 m² | ~2392g | **307 g/m²** |

For comparison: a typical cellular/sport kite flies reliably around
80–150 g/m². The classic 10-cell straws-and-string Instructables kite
comes in around 127 g/m² — light because straws and thread are far
lighter than 6mm rod plus a PLA hub. At 1-2m scale, 6mm rod pushes this
design 3-5x over that.

### The lightweight preset (4mm rod) fixes most of it

All three hub files already expose `strut_d` as a parameter, so switching
rod diameter doesn't require editing the `.scad` geometry — but the hub
should also shrink to match, or you're carrying unnecessary plastic weight.
`3d/validate_and_export.sh` now exports both presets automatically:

| Parameter | Default preset | Lightweight preset |
|---|---|---|
| `strut_d` | 6.0mm | **4.0mm** |
| `hub_r` (exterior / interior / triple) | 12 / 14 / 16mm | **9 / 10 / 11mm** |
| `wall` | 2.5mm | **2.0mm** |
| `strut_depth` | 16.0mm | **12.0mm** |

Verified by direct STL volume measurement: this cuts hub weight by
**56–65%** (exterior 3.6g→1.6g, interior 5.7g→2.3g, triple 8.3g→2.9g).
Combined with switching strut material to thin carbon rod (4mm, ~5g/m,
vs. 6mm solid rod at ~20-40g/m):

| Strut length | Base width | Sail area | Total weight (4mm carbon) | Wing loading |
|---|---|---|---|---|
| 375mm | 1.5m | 1.95 m² | ~416g | **214 g/m²** |
| 500mm | 2.0m | 3.46 m² | ~561g | **162 g/m²** |
| 750mm | 3.0m | 7.79 m² | ~908g | **116 g/m²** |
| 1000mm | 4.0m | 13.86 m² | ~1334g | **96 g/m²** |

Still heavier than a sport kite, but genuinely flyable — in more wind than
a light single-line kite needs, which lines up with the wind-speed
guidance below. Get the lightweight STL/3MF files from
[`3d/printable/lightweight/`](3d/printable/lightweight/), or override the
parameters yourself at export time (see the comment block at the top of
each `.scad` file's parameter section for the exact `-D` flags).

### Why loading gets *better*, not worse, at larger sizes

Counter-intuitively, this design's wing loading improves as it scales up:
hub count is fixed by the layer count (34 real joints for this 4-layer
example, regardless of strut length), but sail area grows with the
*square* of strut length. So a bigger build "dilutes" the fixed hub weight
across more sail area. Don't assume a smaller kite is automatically
lighter-flying — check the actual numbers for your size.

---

## Line strength

Using the standard kite force equation (F = ½ρv²A·Cl, air density
1.225 kg/m³, Cl≈0.8 as a typical estimate for a cellular kite at a good
flying angle — not a measured value for this specific design) on the
lightweight 2m-base example (3.46 m² sail):

| Wind | Line tension |
|---|---|
| 12 km/h (7 mph, Beaufort 3 low) | ~19 N (4 lbf) |
| 19 km/h (12 mph, Beaufort 3 high) | ~47 N (11 lbf) |
| 28 km/h (17 mph, Beaufort 4 high) | ~103 N (23 lbf) |

**Recommendation: use line rated for at least 300N / ~30kgf / ~70 lbf** —
roughly 3x the peak expected steady load at the top of the recommended
wind range, to cover gusts. A mid-weight braided kite line (100-200 lb
test) is the practical choice; sewing thread or fine twine is not strong
enough at this kite's size.

---

## Wind speed and launch

### Wind range

Cross-checked against standard kite wind-range convention (Beaufort scale)
rather than a simplified force-balance estimate alone, since a heavier,
more rigid frame behaves differently from a light single-line kite at the
theoretical minimum:

- **Beaufort 3, 12-19 km/h (8-12 mph)** — realistic minimum for this build,
  even at the lightweight preset
- **Beaufort 4, 20-28 km/h (13-18 mph)** — comfortable sustained flying
  range
- **Above Beaufort 5 (29+ km/h)** — avoid; risk of overloading the printed
  PLA hubs, which aren't designed for shock loads

If it's not launching reliably below 12 km/h, that's expected — this is
not a light-air kite, especially at the default (6mm rod) preset. Don't
mistake "not enough wind" for a structural or assembly problem.

### Launch — 2 person

1. **Person A** holds the kite by the frame (not the sail), facing it
   downwind so the sail catches the wind, standing about 15-20m from
   Person B.
2. **Person B** holds the line spool/handle, facing the kite, wind at
   their back.
3. On a wind gust, A releases the kite while B walks or jogs backward a
   few steps to add relative airspeed, paying out line as the kite climbs.
4. Once climbing steadily, B stops moving and manages line tension from a
   fixed position.

A single-person launch is possible (prop the kite against something
facing into the wind, then walk back with the line and pull to launch),
but two people makes it much more reliable for a frame this size, since
someone needs to hold and orient it against the wind at release.

---

## Summary — what to check before your first flight

- [ ] Line attached to a **Layer 0 base-corner exterior hub** (red, not the
      top apex)
- [ ] Weighed the actual assembled kite and checked wing loading against
      the tables above (don't rely on the estimates alone — measure it)
- [ ] If over ~1m, printed the **lightweight preset**
      (`3d/printable/lightweight/`) with thin (3-4mm) struts, not the 6mm
      default
- [ ] Line rated for **300N+ / 70+ lbf**, not thread or fine twine
- [ ] Flying in **12-28 km/h (8-18 mph)** wind, not below or above that
- [ ] Two people for launch, if the kite is large enough that one person
      can't hold it steady against the wind while releasing

---

Open source · MIT licence (same as the parent repository)
