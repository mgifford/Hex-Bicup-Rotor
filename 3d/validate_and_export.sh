#!/usr/bin/env bash
# Validates printable VINDSNURR hub/jig .scad files and exports STL + 3MF.
#
# Usage: ./validate_and_export.sh
#
# For each printable file (hub_apex, hub_ring, hub_test_jig):
#   1. Renders at the file's committed $fn to confirm the geometry is a
#      manifold solid (this is the "validation" — non-manifold geometry
#      is what produces broken/unprintable meshes).
#   2. Exports STL + 3MF at high resolution ($fn=128) into 3d/printable/
#      for actual printing, without editing the source files.
#
# 3d/printable/ is committed to the repo so anyone can download ready-to-print
# files directly from GitHub without installing OpenSCAD. Re-run this script
# after any geometry change to keep those files current.
#
# Requires OpenSCAD on PATH (brew install --cask openscad@snapshot).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/printable"
OPENSCAD="${OPENSCAD_BIN:-openscad}"

PRINT_FILES=(hub_apex hub_ring hub_test_jig)

mkdir -p "$OUT_DIR"

fail=0

for f in "${PRINT_FILES[@]}"; do
    src="$SCRIPT_DIR/${f}.scad"
    echo "=== Validating ${f}.scad ==="
    if ! "$OPENSCAD" -o /dev/null --export-format=binstl "$src" 2>&1 | tee /tmp/vindsnurr_validate_${f}.log \
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
    echo "One or more files failed validation. See logs in /tmp/vindsnurr_validate_*.log"
    exit 1
fi

echo "All files validated and exported to $OUT_DIR"
