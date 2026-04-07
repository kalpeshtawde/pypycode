#!/bin/bash

# PyPyCode.com Deployment Script
# This script deploys the application to your production server

set -e

echo "🚀 Starting PyPyCode.com deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.server to .env and configure it."
    exit 1
fi

# Check if SSL certificates exist
if [ ! -d nginx/ssl ]; then
    echo "⚠️  SSL directory not found. Creating placeholder..."
    mkdir -p nginx/ssl
    echo "📝 Please place your SSL certificates in nginx/ssl/:"
    echo "   - fullchain.pem"
    echo "   - privkey.pem"
    echo "   You can get free certificates from Let's Encrypt using certbot."
fi

# Stop existing containers if they exist
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose -f docker-compose.prod.yml ps

# Show logs
echo "📋 Showing recent logs..."
docker-compose -f docker-compose.prod.yml logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 Your application should be available at:"
echo "   HTTP: http://pypycode.com:8084"
echo "   HTTPS: https://pypycode.com:8446"
echo ""
echo "📝 Next steps:"
echo "   1. Configure your reverse proxy to forward pypycode.com:80 → localhost:8084"
echo "   2. Configure your reverse proxy to forward pypycode.com:443 → localhost:8446"
echo "   3. Update DNS to point pypycode.com to your server"
