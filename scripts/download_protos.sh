#!/bin/bash

set -e  # Exit on error

# Colors for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

DEST_DIR="proto_definitions/dota2"
API_URL="https://api.github.com/repos/SteamDatabase/Protobufs/contents/dota2"

# Optional: set GITHUB_TOKEN env var to avoid API rate limits (60 req/hr unauthenticated)
AUTH_HEADER=""
if [ -n "$GITHUB_TOKEN" ]; then
    AUTH_HEADER="-H \"Authorization: Bearer $GITHUB_TOKEN\""
    echo -e "${YELLOW}Using GITHUB_TOKEN for authenticated requests.${NC}"
fi

echo -e "${GREEN}Downloading Dota 2 proto files from SteamDatabase...${NC}"

mkdir -p "$DEST_DIR"

# Fetch file list via GitHub API — use python3 to parse JSON properly
echo -e "${YELLOW}Fetching file list from GitHub API...${NC}"
API_RESPONSE=$(curl -sf ${AUTH_HEADER:+"-H" "Authorization: Bearer $GITHUB_TOKEN"} "$API_URL") || {
    echo -e "${RED}Failed to reach GitHub API. Check your internet connection.${NC}"
    exit 1
}

# Check for rate limit error
if echo "$API_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if isinstance(d, list) else 1)" 2>/dev/null; then
    : # OK, it's a list
else
    echo -e "${RED}GitHub API error:${NC}"
    echo "$API_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('message','Unknown error'))"
    echo "Tip: set GITHUB_TOKEN env var to avoid rate limits."
    exit 1
fi

# Extract name and download_url pairs using python3 (safe JSON parsing)
FILE_INFO=$(echo "$API_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for f in data:
    if f['type'] == 'file' and f['name'].endswith('.proto'):
        print(f['name'] + '|' + f['download_url'])
" | sort)

if [ -z "$FILE_INFO" ]; then
    echo -e "${RED}No .proto files found in API response.${NC}"
    exit 1
fi

FILE_COUNT=$(echo "$FILE_INFO" | wc -l | tr -d ' ')
echo -e "${YELLOW}Found $FILE_COUNT proto files.${NC}"

DOWNLOADED=0
SKIPPED=0
FAILED=0

while IFS='|' read -r filename url; do
    dest="$DEST_DIR/$filename"

    # Skip if already downloaded (use --force flag to re-download)
    if [ -f "$dest" ] && [ "${FORCE:-0}" != "1" ]; then
        echo "  $filename ... skipped (already exists)"
        ((SKIPPED++))
        continue
    fi

    echo -n "  $filename ... "
    if curl -sf -o "$dest" "$url"; then
        echo -e "${GREEN}✓${NC}"
        ((DOWNLOADED++))
    else
        echo -e "${RED}✗ (failed)${NC}"
        ((FAILED++))
    fi
done <<< "$FILE_INFO"

echo ""
echo -e "${GREEN}Downloaded: $DOWNLOADED${NC}"
[ "$SKIPPED" -gt 0 ] && echo -e "${YELLOW}Skipped (already exist): $SKIPPED${NC}"
[ "$FAILED"  -gt 0 ] && echo -e "${RED}Failed: $FAILED${NC}"

echo ""
TOTAL=$(ls -1 "$DEST_DIR"/*.proto 2>/dev/null | wc -l | tr -d ' ')
echo "Total proto files in $DEST_DIR: $TOTAL"

echo ""
echo -e "${GREEN}Next step:${NC}"
echo "  python scripts/compile_protos.py"
echo ""
echo "Tip: to force re-download all files, run:"
echo "  FORCE=1 bash scripts/download_protos.sh"
