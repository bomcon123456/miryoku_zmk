#!/usr/bin/env bash
# Regenerate docs/keymap/totem.svg from the miryoku layer macros.
# Usage: docs/keymap/build.sh   (or: make -C docs/keymap)
set -euo pipefail
cd "$(dirname "$0")"

VENV=.venv
if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q keymap-drawer pyyaml
fi

"$VENV/bin/python" gen_yaml.py
"$VENV/bin/keymap" draw totem.yaml > totem.svg
echo "wrote $(pwd)/totem.svg"
