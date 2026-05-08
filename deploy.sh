#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=== Business Digest — Deploy ==="

# 1. Generate fresh content
echo ""
echo "--- Generating content ---"
python3 run.py --mode all

# 2. Send newsletter
echo ""
echo "--- Sending newsletter ---"
python3 run.py --mode send

# 3. Deploy landing page (copy to a web-served directory)
LANDING_DEST="${DEPLOY_DIR:-/tmp/opencode/landing}"
mkdir -p "$LANDING_DEST"
cp templates/landing.html "$LANDING_DEST/index.html"
echo "Landing page copied to $LANDING_DEST/index.html"

# 4. Archive output
ARCHIVE_DIR="archive/$(date +%Y/%m)"
mkdir -p "$ARCHIVE_DIR"
cp output/newsletters/*.html "$ARCHIVE_DIR/" 2>/dev/null || true
cp output/scripts/*.txt "$ARCHIVE_DIR/" 2>/dev/null || true
echo "Output archived to $ARCHIVE_DIR"

echo ""
echo "=== Deploy complete ==="
echo "Newsletter: $(ls -t output/newsletters/*.html 2>/dev/null | head -1)"
echo "Landing:    $LANDING_DEST/index.html"
