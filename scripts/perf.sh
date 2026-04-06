#!/usr/bin/env bash
set -e

echo "⚡ PyPyCode — performance stack startup"
echo "======================================="

echo "→ Building sandbox image..."
docker build -t pypycode-sandbox:latest ./sandbox

echo "→ Starting perf services..."
docker compose -f docker-compose.perf.yml up -d --build db_perf redis_perf api_perf worker_perf

echo "→ Waiting for perf Postgres..."
until docker compose -f docker-compose.perf.yml exec db_perf pg_isready -U pypycode -q; do sleep 1; done

echo "→ Running migrations on perf DB..."
docker compose -f docker-compose.perf.yml exec api_perf flask --app app db upgrade

echo "→ Seeding perf DB..."
docker compose -f docker-compose.perf.yml exec api_perf python seed.py

echo "→ Running JMeter test plan..."
docker compose -f docker-compose.perf.yml run --rm jmeter

echo ""
echo "✅ Perf test complete"
echo "   Results JTL:  perf/results/results.jtl"
echo "   HTML report:  perf/results/report/index.html"
