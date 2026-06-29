#!/usr/bin/env bash
# QuickForge launcher — sets up venv on first run
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV" ]; then
  echo "Setting up QuickForge environment..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
  echo "Ready."
  echo ""
fi

exec "$VENV/bin/python" "$SCRIPT_DIR/cli.py" "$@"
