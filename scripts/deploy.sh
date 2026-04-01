#!/usr/bin/env bash
set -e

echo "🚀 PyPyCode — production deploy"
echo "================================"

if [ ! -f .env ]; then
  echo "❌ .env file not found. Copy .env.example and fill in values."
  exit 1
fi

source .env

echo "→ Building sandbox image..."
docker build -t pypycode-sandbox:latest ./sandbox

echo "→ Building and starting production stack..."
docker compose -f docker-compose.prod.yml up -d --build

echo "→ Waiting for DB..."
until docker compose -f docker-compose.prod.yml exec db pg_isready -U "$POSTGRES_USER" -q; do
  sleep 2
done

echo "→ Running migrations..."
docker compose -f docker-compose.prod.yml exec api flask --app app db upgrade

echo ""
echo "✅ Deployed!"
echo "   Make sure your domain DNS points to this server."
echo "   SSL certs should be in ./nginx/ssl/fullchain.pem and privkey.pem"
echo "   (use certbot: certbot certonly --standalone -d yourdomain.com)"
