# Sitemap URL Fix

## Problem

The sitemap URLs were not accessible:
- `https://your-domain.com/sitemap.xml` → 404 or not found
- `https://your-domain.com/sitemap-problems.xml` → 404 or not found

## Root Cause

The Flask backend routes for sitemaps were registered at the root level (`/sitemap.xml`), but Nginx was only proxying specific paths to the Flask API:
- `/api/` → Flask API
- `/admin` → Flask Admin

All other requests were being sent to the frontend (Vite dev server or static files), which doesn't have the sitemap routes.

## Solution

Added Nginx location blocks to route sitemap requests to the Flask backend.

### Files Modified

1. **`nginx/nginx.dev.conf`** (Development)
   - Added `location ~ ^/sitemap.*\.xml$` to proxy sitemap requests to Flask
   - Added `location = /robots.txt` to serve robots.txt from frontend

2. **`nginx/nginx.prod.conf`** (Production)
   - Added `location ~ ^/sitemap.*\.xml$` to proxy sitemap requests to Flask
   - Added `location = /robots.txt` to serve robots.txt from static files
   - Moved SPA routing to the end (must be last for proper precedence)

3. **`nginx/nginx.server.conf`** (Server/Production)
   - Added `location ~ ^/sitemap.*\.xml$` to proxy sitemap requests to Flask
   - Added `location = /robots.txt` to serve robots.txt from static files
   - Moved SPA routing to the end

## How It Works

**Before:**
```
Request: GET /sitemap.xml
↓
Nginx checks locations (in order):
  - /admin? No
  - /api/? No
  - / (catch-all) → Sends to frontend
↓
Frontend doesn't have /sitemap.xml
↓
404 Not Found
```

**After:**
```
Request: GET /sitemap.xml
↓
Nginx checks locations (in order):
  - /sitemap.*\.xml? YES! ✓
  - Proxy to Flask API (http://api:5000)
↓
Flask returns XML sitemap
↓
200 OK + XML content
```

## Testing

### Local Development

1. Restart Docker containers:
   ```bash
   docker-compose restart nginx
   ```

2. Test the URLs:
   ```bash
   curl http://localhost:81/sitemap.xml
   curl http://localhost:81/sitemap-problems.xml
   curl http://localhost:81/robots.txt
   ```

3. Expected response: XML content with proper `<?xml version="1.0"?>` header

### Production

1. Reload Nginx:
   ```bash
   docker exec pypycode_nginx_1 nginx -s reload
   # or
   sudo systemctl reload nginx
   ```

2. Test the URLs:
   ```bash
   curl https://your-domain.com/sitemap.xml
   curl https://your-domain.com/sitemap-problems.xml
   curl https://your-domain.com/robots.txt
   ```

## Nginx Location Block Explanation

```nginx
# Regex location for all sitemap files
location ~ ^/sitemap.*\.xml$ {
  proxy_pass http://api;  # Send to Flask backend
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

- `~` = case-sensitive regex match
- `^/sitemap.*\.xml$` = matches `/sitemap.xml`, `/sitemap-problems.xml`, etc.
- `proxy_pass http://api` = sends to Flask API upstream
- Headers = preserve client IP and host information

## Location Block Precedence

Nginx checks location blocks in this order:
1. **Exact match** (`=`) - highest priority
2. **Prefix match** (`^~`) - stops searching if matched
3. **Regex match** (`~`, `~*`) - checked in order
4. **Prefix match** (no modifier) - lowest priority

**Our order in the config:**
```nginx
location ~ ^/sitemap.*\.xml$ { ... }  # Regex - checked early
location = /robots.txt { ... }        # Exact - highest priority
location /api/ { ... }                # Prefix
location / { ... }                    # Catch-all - last
```

This ensures sitemaps are caught before the catch-all `/` location.

## Verification Checklist

- [ ] Nginx configs updated (dev, prod, server)
- [ ] Docker containers restarted or Nginx reloaded
- [ ] `/sitemap.xml` returns 200 with XML content
- [ ] `/sitemap-problems.xml` returns 200 with XML content
- [ ] `/robots.txt` returns 200 with text content
- [ ] Google Search Console can fetch sitemaps
- [ ] No 404 errors in Nginx logs

## Nginx Logs

If still having issues, check Nginx logs:

```bash
# Docker
docker logs pypycode_nginx_1 | tail -50

# Server
sudo tail -50 /var/log/nginx/error.log
sudo tail -50 /var/log/nginx/access.log
```

Look for:
- `502 Bad Gateway` - Flask API not responding
- `404 Not Found` - Route not found in Flask
- `Connection refused` - Nginx can't reach Flask

## Related Files

- `backend/app/routes/seo.py` - Flask sitemap routes
- `backend/app/__init__.py` - Blueprint registration
- `frontend/public/robots.txt` - Robots file
- `frontend/src/utils/seo.ts` - SEO utilities

---

**Status:** ✅ Fixed  
**Date:** July 12, 2024
