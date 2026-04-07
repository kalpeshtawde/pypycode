# PyPyCode.com Deployment Guide

This guide explains how to deploy PyPyCode.com on your existing server with multiple websites.

## Prerequisites

- Docker and Docker Compose installed
- PostgreSQL already running on the server
- Domain pypycode.com pointing to your server
- SSL certificates (can use Let's Encrypt)

## Port Allocation

To avoid conflicts with existing containers, PyPyCode.com uses:
- **HTTP**: 8084 (internal) → 80 (external via reverse proxy)
- **HTTPS**: 8446 (internal) → 443 (external via reverse proxy)

## Quick Deployment

1. **Configure Environment**
   ```bash
   cp .env.server .env
   # Edit .env with your actual database password and secrets
   ```

2. **Set up SSL Certificates**
   ```bash
   mkdir -p nginx/ssl
   # Place your certificates in nginx/ssl/
   # - fullchain.pem
   # - privkey.pem
   ```

3. **Deploy**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## Database Setup

Since PostgreSQL is already installed on your server:

1. **Create database and user:**
   ```sql
   CREATE DATABASE pypycode;
   CREATE USER pypycode WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE pypycode TO pypycode;
   ```

2. **Update .env file:**
   ```
   DATABASE_URL=postgresql://pypycode:your_secure_password@localhost:5432/pypycode
   ```

## Reverse Proxy Configuration

Add this to your main reverse proxy (nginx/apache):

### Nginx Example
```nginx
server {
    listen 80;
    server_name pypycode.com www.pypycode.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name pypycode.com www.pypycode.com;

    # Your SSL certificates
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;

    location / {
        proxy_pass http://localhost:8084;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Container Management

### Start services
```bash
docker-compose -f docker-compose.server.yml up -d
```

### Stop services
```bash
docker-compose -f docker-compose.server.yml down
```

### View logs
```bash
docker-compose -f docker-compose.server.yml logs -f
```

### Update application
```bash
git pull
docker-compose -f docker-compose.server.yml up --build -d
```

## Container Names

The deployed containers use these names to avoid conflicts:
- `pypycode_nginx`
- `pypycode_api`
- `pypycode_worker`
- `pypycode_redis`
- `pypycode_frontend_builder`

## Security Notes

- Change all default passwords in .env
- Use strong SSL certificates
- Keep Docker images updated
- Monitor logs regularly
- Set up database backups

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U pypycode -d pypycode
```

### Port Conflicts
```bash
# Check what's using ports
netstat -tulpn | grep :8084
netstat -tulpn | grep :8446
```

### SSL Issues
```bash
# Check SSL certificates
openssl x509 -in nginx/ssl/fullchain.pem -text -noout
```

## Monitoring

Set up monitoring for:
- Container health
- Database performance
- SSL certificate expiration
- Disk space usage

## Backup Strategy

1. **Database backups:**
   ```bash
   pg_dump -h localhost -U pypycode pypycode > backup.sql
   ```

2. **Application data:**
   - Redis data volume
   - User uploaded content (if any)

3. **Configuration backups:**
   - .env file
   - nginx configuration
   - SSL certificates
