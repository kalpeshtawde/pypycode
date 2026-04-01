#!/usr/bin/env bash
set -e

echo "🐍 PyPyCode — local dev startup"
echo "================================"

# Build sandbox image first
echo "→ Building sandbox image..."
docker build -t pypycode-sandbox:latest ./sandbox

# Start all services
echo "→ Starting services..."
docker compose up -d --build

# Wait for DB
echo "→ Waiting for Postgres..."
until docker compose exec db pg_isready -U pypycode -q; do sleep 1; done

# Run migrations
echo "→ Running migrations..."
docker compose exec api flask --app app db upgrade

# Seed database
echo "→ Seeding problems..."
docker compose exec api python seed.py

echo ""
echo "✅ PyPyCode is running!"
echo "   App:      http://localhost:81"
echo "   Flower:   http://localhost:5555"
echo "   DB:       localhost:5432"
echo ""
echo "Demo login: demo@pypycode.dev / demo1234"
