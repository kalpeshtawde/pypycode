.PHONY: sync-remote-db sync-remote-db-confirm delete-local-user create-perfuser perf-test

PG15_BIN ?= /opt/homebrew/opt/postgresql@15/bin
DATABASE_URL ?= postgresql://pypycode:pypycode@127.0.0.1:5432/pypycode
FLASK_APP ?= app
ENV_FILE ?= .env.db-sync
PASSWORD ?= cvq8RUNEcCugrxcFbe6p

sync-remote-db:
	PATH="$(PG15_BIN):$$PATH" DATABASE_URL="$(DATABASE_URL)" flask --app $(FLASK_APP) sync-remote-db --env-file $(ENV_FILE) --yes

sync-remote-db-confirm:
	PATH="$(PG15_BIN):$$PATH" DATABASE_URL="$(DATABASE_URL)" flask --app $(FLASK_APP) sync-remote-db --env-file $(ENV_FILE)

# Usage: make delete-local-user EMAIL=user@example.com
delete-local-user:
	@test -n "$(EMAIL)" || (echo "ERROR: EMAIL is required. Usage: make delete-local-user EMAIL=user@example.com" && exit 1)
	docker compose -f ../docker-compose.yml exec api python delete_local_user.py $(EMAIL)

# Usage: make create-perfuser [PASSWORD=your_password]
create-perfuser:
	docker compose -f ../docker-compose.yml exec -e PERF_USER_PASSWORD=$(PASSWORD) api python create_perfuser.py

# Usage: make perf-test
perf-test:
	bash ../perf/playwright/run.sh
