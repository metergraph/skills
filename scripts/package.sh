#!/bin/sh
# Builds one zip per skill in dist/, in the shape Claude Desktop's
# "Upload a skill" expects: the skill's folder at the top of the archive.
# Also writes dist/SHA256SUMS. Usage: sh scripts/package.sh
set -eu
cd "$(dirname "$0")/.."
rm -rf dist
mkdir dist
cd skills
for dir in */; do
  name="${dir%/}"
  # -X drops extra file attributes, so archives from the same tree are stable.
  zip -q -r -X "../dist/$name.zip" "$name"
done
cd ../dist
if command -v sha256sum >/dev/null 2>&1; then sha256sum ./*.zip > SHA256SUMS; else shasum -a 256 ./*.zip > SHA256SUMS; fi
ls
