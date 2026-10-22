#!/bin/sh
# Build verified regular-file skill archives and SHA256SUMS.
set -eu
cd "$(dirname "$0")/.."
node scripts/validate.mjs
rm -rf dist
python3 scripts/package.py
