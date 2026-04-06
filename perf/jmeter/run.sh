#!/usr/bin/env sh
set -eu

RESULTS_DIR="/results"
TESTS_DIR="/tests"
DEFAULTS_FILE="$TESTS_DIR/defaults.properties"
ADMIN_FILE="$TESTS_DIR/admin.properties"
USED_FILE="$RESULTS_DIR/used.properties"
METADATA_FILE="$RESULTS_DIR/latest-run.json"
REPORT_DIR="$RESULTS_DIR/report"
TEST_PLAN="${JMETER_TEST_PLAN:-/tests/test-plan.jmx}"
CONFIG_URL="${PERF_CONFIG_URL:-}"

mkdir -p "$REPORT_DIR"
cp "$TESTS_DIR/empty.properties" "$ADMIN_FILE"

if [ -n "$CONFIG_URL" ]; then
  curl -fsS "$CONFIG_URL" -o "$ADMIN_FILE" || true
fi

cp "$ADMIN_FILE" "$USED_FILE"
STARTED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

jmeter -n \
  -t "$TEST_PLAN" \
  -q "$DEFAULTS_FILE" \
  -q "$ADMIN_FILE" \
  -l "$RESULTS_DIR/results.jtl" \
  -e -o "$REPORT_DIR"

FINISHED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat > "$METADATA_FILE" <<EOF
{
  "startedAt": "$STARTED_AT",
  "finishedAt": "$FINISHED_AT",
  "resultsJtl": "perf/results/results.jtl",
  "htmlReport": "perf/results/report/index.html",
  "usedProperties": "perf/results/used.properties"
}
EOF
