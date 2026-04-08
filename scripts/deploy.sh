#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="docker-compose.prod.yml"

usage() {
  cat <<EOF
Usage: ./scripts/deploy.sh <mode>

Modes:
  frontend-fast  Build frontend static assets and refresh nginx only (fastest)
  full-stack     Rebuild api/worker/frontend stack, then run DB migrations

Examples:
  ./scripts/deploy.sh frontend-fast
  ./scripts/deploy.sh full-stack
EOF
}

require_env_file() {
  if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy .env.example and fill in values."
    exit 1
  fi
}

deploy_frontend_fast() {
  echo "⚡ Fast frontend deploy"
  echo "→ Building frontend dist locally..."
  (
    cd frontend
    npm ci
    npm run build
  )

  echo "→ Reloading nginx..."
  docker compose -f "$COMPOSE_FILE" up -d nginx
  docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload

  echo "✅ Frontend deployed (fast mode)."
}

deploy_full_stack() {
  echo "🚀 Full-stack deploy"
  echo "→ Building sandbox image..."
  docker build -t pypycode-sandbox:latest ./sandbox

  echo "→ Building and starting production services..."
  docker compose -f "$COMPOSE_FILE" up -d --build api worker nginx redis

  echo "→ Running migrations..."
  docker compose -f "$COMPOSE_FILE" exec api flask --app app db upgrade

  echo "✅ Full-stack deploy complete."
}

main() {
  if [ "${1:-}" = "" ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    usage
    exit 0
  fi

  local mode="$1"

  echo "PyPyCode deployment"
  echo "===================="
  require_env_file

  case "$mode" in
    frontend-fast)
      deploy_frontend_fast
      ;;
    full-stack)
      deploy_full_stack
      ;;
    *)
      echo "❌ Unknown mode: $mode"
      echo ""
      usage
      exit 1
      ;;
  esac
}

main "$@"
