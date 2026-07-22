#!/usr/bin/env bash
# Validates kite_corner.scad and exports STL + 3MF.
#
# Usage: ./validate_and_export.sh
#
# Renders at the file's committed $fn to confirm the geometry is a
# manifold solid (non-manifold geometry produces broken/unprintable
# meshes), then exports STL and 3MF at high resolution ($fn=128)
# into kite-corners/printable/, without editing the source file.
#
# kite-corners/printable/ is committed to the repo so anyone can download
# ready-to-print files directly from GitHub without installing OpenSCAD.
# Re-run this script after any geometry change to keep those files current.
#
# Requires OpenSCAD on PATH (brew install --cask openscad@snapshot).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/printable"
OPENSCAD="${OPENSCAD_BIN:-openscad}"

PRINT_FILES=(kite_corner)

mkdir -p "$OUT_DIR"

fail=0

for f in "${PRINT_FILES[@]}"; do
    src="$SCRIPT_DIR/${f}.scad"
    echo "=== Validating ${f}.scad ==="
    if ! "$OPENSCAD" -o /dev/null --export-format=binstl "$src" 2>&1 | tee /tmp/kite_corner_validate_${f}.log \
        | grep -q "Status:     NoError"; then
        echo "VALIDATION FAILED: ${f}.scad did not render as a clean manifold solid."
        fail=1
        continue
    fi
    echo "OK: ${f}.scad is a manifold solid."

    echo "--- Exporting ${f} (STL + 3MF, \$fn=128) ---"
    "$OPENSCAD" -o "$OUT_DIR/${f}.stl" -D '$fn=128' --export-format=binstl "$src"
    "$OPENSCAD" -o "$OUT_DIR/${f}.3mf" -D '$fn=128' "$src"
    echo ""
done

if [ "$fail" -ne 0 ]; then
    echo "One or more files failed validation. See logs in /tmp/kite_corner_validate_*.log"
    exit 1
fi

echo "All files validated and exported to $OUT_DIR"
