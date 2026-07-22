#!/usr/bin/env bash
# Validates the kite corner hub .scad files and exports STL + 3MF, at both
# the default (6mm rod) and lightweight (4mm rod) parameter presets.
#
# Usage: ./validate_and_export.sh
#
# Renders each file at its committed $fn to confirm the geometry is a
# manifold solid (non-manifold geometry produces broken/unprintable
# meshes), then exports STL and 3MF at high resolution ($fn=128):
#   - kite-corners/3d/printable/            — default preset, 6mm rod
#   - kite-corners/3d/printable/lightweight/ — 4mm rod, smaller hub_r/wall
#     (see FLIGHT.md "Weight budget" for why a 1m+ kite needs this)
# without editing the source files (overrides passed via -D).
#
# Both printable/ directories are committed to the repo so anyone can
# download ready-to-print files directly from GitHub without installing
# OpenSCAD. Re-run this script after any geometry change to keep those
# files current.
#
# Requires OpenSCAD on PATH (brew install --cask openscad@snapshot).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/printable"
LIGHT_OUT_DIR="$OUT_DIR/lightweight"
OPENSCAD="${OPENSCAD_BIN:-openscad}"

PRINT_FILES=(kite_corner kite_corner_interior kite_corner_triple)

# lightweight hub_r per file — sized so 4mm+0.3mm-tol sockets keep clear
# spacing at a smaller sphere radius (verified: exit-point spacing exceeds
# socket diameter with margin at these values). Parallel array indexed by
# position in PRINT_FILES (not an associative array — macOS ships bash 3.2
# by default, which doesn't support `declare -A`).
LIGHT_HUB_R=(9.0 10.0 11.0)

mkdir -p "$OUT_DIR" "$LIGHT_OUT_DIR"

fail=0

# validate_render(): runs OpenSCAD to a log file, then greps the file
# afterward, rather than piping OpenSCAD's live output through `tee | grep
# -q`. The live-pipe form is flaky under `set -o pipefail`: if grep -q
# finds its match and closes its read end before OpenSCAD/tee finish
# flushing, OpenSCAD can be signalled (SIGPIPE) and exit non-zero, which
# pipefail then reports as the whole pipeline failing even though the
# render genuinely succeeded (reproduced directly: ~1-in-8 runs failed
# with a log that clearly showed "Status: NoError"). Writing to a file
# first removes the race entirely.
validate_render() {
    local desc="$1" logfile="$2"; shift 2
    "$OPENSCAD" "$@" > "$logfile" 2>&1
    if ! grep -q "Status:     NoError" "$logfile"; then
        echo "VALIDATION FAILED: $desc did not render as a clean manifold solid. See $logfile"
        return 1
    fi
    echo "OK: $desc is a manifold solid."
}

for i in "${!PRINT_FILES[@]}"; do
    f="${PRINT_FILES[$i]}"
    light_hub_r="${LIGHT_HUB_R[$i]}"
    src="$SCRIPT_DIR/${f}.scad"

    echo "=== Validating ${f}.scad (default preset) ==="
    if ! validate_render "${f}.scad" "/tmp/kite_corner_validate_${f}.log" \
        -o /dev/null --export-format=binstl "$src"; then
        fail=1
        continue
    fi

    echo "--- Exporting ${f} (STL + 3MF, \$fn=128, default 6mm-rod preset) ---"
    "$OPENSCAD" -o "$OUT_DIR/${f}.stl" -D '$fn=128' --export-format=binstl "$src"
    "$OPENSCAD" -o "$OUT_DIR/${f}.3mf" -D '$fn=128' "$src"

    echo "=== Validating ${f}.scad (lightweight 4mm-rod preset, hub_r=${light_hub_r}) ==="
    if ! validate_render "${f}.scad (lightweight preset)" "/tmp/kite_corner_validate_${f}_light.log" \
        -o /dev/null --export-format=binstl \
        -D 'strut_d=4.0' -D "hub_r=${light_hub_r}" -D 'wall=2.0' -D 'strut_depth=12.0' "$src"; then
        fail=1
        continue
    fi

    echo "--- Exporting ${f} (STL + 3MF, \$fn=128, lightweight 4mm-rod preset) ---"
    "$OPENSCAD" -o "$LIGHT_OUT_DIR/${f}.stl" -D '$fn=128' \
        -D 'strut_d=4.0' -D "hub_r=${light_hub_r}" -D 'wall=2.0' -D 'strut_depth=12.0' \
        --export-format=binstl "$src"
    "$OPENSCAD" -o "$LIGHT_OUT_DIR/${f}.3mf" -D '$fn=128' \
        -D 'strut_d=4.0' -D "hub_r=${light_hub_r}" -D 'wall=2.0' -D 'strut_depth=12.0' \
        "$src"
    echo ""
done

if [ "$fail" -ne 0 ]; then
    echo "One or more files failed validation. See logs in /tmp/kite_corner_validate_*.log"
    exit 1
fi

echo "All files validated and exported to $OUT_DIR and $LIGHT_OUT_DIR"
