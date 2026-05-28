#!/usr/bin/env bash
# Run Playwright perf tests against a local dev environment.
# Usage:
#   ./perf/playwright/run.sh
#   HEADLESS=false ./perf/playwright/run.sh   # headed (watch the browser)
#   SLOW_MO_MS=300 ./perf/playwright/run.sh   # slow motion for debugging
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env.local"

if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: $ENV_FILE not found."
    echo "Copy $SCRIPT_DIR/.env.example to $SCRIPT_DIR/.env.local and fill in your credentials."
    exit 1
fi

pip install -q -r "$SCRIPT_DIR/requirements.txt"
playwright install chromium --with-deps 2>/dev/null || playwright install chromium

echo ""
python "$SCRIPT_DIR/perf_test.py" "$@"
