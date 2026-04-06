# 🐍 PyPyCode

> A Python-only coding challenge platform — like LeetCode, but focused entirely on Python.

Built with **Flask · React · TypeScript · Celery · Docker · PostgreSQL · Redis**.

---

## Architecture

```
Browser → Nginx → React SPA (frontend)
                → Flask API (backend)
                     → PostgreSQL (data)
                     → Redis (cache + sessions)
                     → Celery (job queue)
                          → Docker sandbox (isolated Python execution)
```

---

## Quick Start (local dev)

### Prerequisites
- Docker + Docker Compose
- ~4 GB RAM free

### 1. Clone & run

```bash
git clone https://github.com/you/pypycode.git
cd pypycode
chmod +x scripts/dev.sh
./scripts/dev.sh
```

This will:
1. Build the hardened Python sandbox image
2. Start all services (Nginx, React, Flask, Celery, Redis, Postgres, Flower)
3. Run DB migrations
4. Seed 8 sample problems + a demo user

### 2. Open the app

| Service   | URL                       |
|-----------|---------------------------|
| App       | http://localhost:81        |
| Flower    | http://localhost:5555      |
| Postgres  | localhost:5432             |

**Demo login:** `demo@pypycode.dev` / `demo1234`

---

## Project Structure

```
pypycode/
├── docker-compose.yml          # Local dev
├── docker-compose.prod.yml     # Production
├── .env.example                # Copy to .env for prod
│
├── nginx/
│   ├── nginx.dev.conf
│   └── nginx.prod.conf
│
├── sandbox/
│   ├── Dockerfile              # Hardened Python image
│   └── runner.py               # Test case executor
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── seed.py                 # Seeds 8 problems + demo user
│   └── app/
│       ├── __init__.py         # Flask app factory + Celery
│       ├── models/__init__.py  # User, Problem, Submission
│       ├── routes/
│       │   ├── auth.py         # /auth/register, /login, /me
│       │   ├── problems.py     # /problems/
│       │   ├── submissions.py  # /submissions/
│       │   └── leaderboard.py  # /leaderboard/
│       └── services/
│           └── runner.py       # Celery task → Docker sandbox
│
└── frontend/
    ├── index.html
    ├── vite.config.ts
    ├── tailwind.config.ts
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── index.css
        ├── types/index.ts
        ├── hooks/useAuth.ts    # Zustand auth store
        ├── utils/api.ts        # Typed fetch wrapper
        ├── components/
        │   └── Layout.tsx      # Navbar + footer
        └── pages/
            ├── HomePage.tsx
            ├── ProblemsPage.tsx
            ├── ProblemPage.tsx  # Monaco editor + submission
            ├── LeaderboardPage.tsx
            └── AuthPage.tsx
```

---

## API Reference

### Auth
| Method | Endpoint          | Auth | Description        |
|--------|-------------------|------|--------------------|
| POST   | /auth/register    | —    | Register new user  |
| POST   | /auth/login       | —    | Login, get JWT     |
| GET    | /auth/me          | JWT  | Current user info  |

### Problems
| Method | Endpoint          | Auth | Description        |
|--------|-------------------|------|--------------------|
| GET    | /problems/        | —    | List all problems  |
| GET    | /problems/:slug   | —    | Get single problem |
| POST   | /problems/        | JWT  | Create problem     |

### Submissions
| Method | Endpoint                    | Auth | Description           |
|--------|-----------------------------|------|-----------------------|
| POST   | /submissions/               | JWT  | Submit code           |
| GET    | /submissions/:id            | JWT  | Poll result           |
| GET    | /submissions/problem/:slug  | JWT  | My submissions        |

### Leaderboard
| Method | Endpoint       | Auth | Description     |
|--------|----------------|------|-----------------|
| GET    | /leaderboard/  | —    | Top 50 by solved|

---

## Sandbox Security

User code runs in a throw-away Docker container with:

| Restriction        | Value                          |
|--------------------|-------------------------------|
| Network            | Disabled (`--network none`)   |
| Memory             | 256 MB hard limit             |
| CPU                | 0.5 cores max                 |
| Execution timeout  | 5 seconds                     |
| Filesystem         | Read-only                     |
| User               | Non-root (`runner`, uid 1001) |
| Syscalls           | seccomp default profile       |
| Resource limits    | `RLIMIT_CPU`, `RLIMIT_AS`, `RLIMIT_NOFILE` via Python |

---

## Production Deployment

### 1. Prepare server

```bash
# On your server (Ubuntu 22.04+)
apt update && apt install -y docker.io docker-compose-plugin certbot
```

### 2. SSL certificate

```bash
certbot certonly --standalone -d yourdomain.com
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
```

### 3. Configure env

```bash
cp .env.example .env
# Edit .env with real secrets
nano .env
```

### 4. Deploy

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 5. Seed (first deploy only)

```bash
docker compose -f docker-compose.prod.yml exec api python seed.py
```

---

## Performance Testing (JMeter)

This repo now includes a dedicated perf stack with isolated database + Redis:

- `docker-compose.perf.yml`
- `db_perf` (Postgres, port `5433`)
- `redis_perf` (Redis, port `6380`)
- `api_perf` (`APP_CONFIG=perf`)
- `worker_perf` (Celery for perf submissions)
- `jmeter` (non-GUI run with HTML report output)

### Perf config profile

Backend supports profile-based config in `backend/app/config.py`:

- `APP_CONFIG=default` → normal `DATABASE_URL`
- `APP_CONFIG=perf` → `PERF_DATABASE_URL` (fallbacks to `DATABASE_URL`)
- Perf pool tuning via:
  - `PERF_SQLALCHEMY_POOL_SIZE` (default `20`)
  - `PERF_SQLALCHEMY_MAX_OVERFLOW` (default `40`)

### Run perf test

```bash
chmod +x scripts/perf.sh
./scripts/perf.sh
```

Outputs:

- `perf/results/results.jtl`
- `perf/results/report/index.html`
- `perf/results/latest-run.json`
- `perf/results/used.properties`

### JMeter plan structure

The plan is in `perf/jmeter/test-plan.jmx` and implements:

- Thread Group (`perf.users`, default 100)
- HTTP Cookie Manager
- POST login request
- POST submission request
- Summary Report + HTML dashboard output

### Admin-panel configurability

Perf test settings are stored in DB (`perf_test_configs`) and editable in Flask-Admin:

- Admin view: **Performance Config**
- Export endpoint for JMeter: `/admin/perf/jmeter.properties`
- Latest run metadata endpoint: `/admin/perf/latest-run`

The JMeter container fetches that properties file before running, so changing values in admin updates future perf runs without editing `.jmx` directly.

`/admin/perf/latest-run` returns:

- `metadata`: parsed contents of `perf/results/latest-run.json` (timestamps and artifact paths)
- `activeConfig`: current enabled perf config snapshot used for future runs

---

## Adding Problems

Problems can be added via the API (POST `/problems/`) or directly via `seed.py`.

Each problem needs:
```json
{
  "slug": "unique-slug",
  "title": "Problem Title",
  "difficulty": "easy | medium | hard",
  "description": "Markdown description",
  "starterCode": "def solution(...):\n    pass",
  "examples": [{ "input": "...", "output": "..." }],
  "testCases": [
    { "function": "solution", "args": [...], "expected": ... }
  ],
  "tags": ["array", "dp"]
}
```

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | React 18, TypeScript, Vite          |
| Styling    | Tailwind CSS                        |
| Editor     | Monaco Editor (VS Code engine)      |
| Fonts      | Fraunces (display), DM Sans (body), JetBrains Mono |
| Backend    | Flask 3, SQLAlchemy, Flask-Migrate  |
| Auth       | JWT (flask-jwt-extended)            |
| Queue      | Celery + Redis                      |
| Sandbox    | Docker (hardened Python container)  |
| Database   | PostgreSQL 16                       |
| Proxy      | Nginx                               |
| Monitoring | Flower (Celery dashboard)           |

---


