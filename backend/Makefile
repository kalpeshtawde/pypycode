.PHONY: sync-remote-db sync-remote-db-confirm

PG15_BIN ?= /opt/homebrew/opt/postgresql@15/bin
DATABASE_URL ?= postgresql://pypycode:pypycode@127.0.0.1:5432/pypycode
FLASK_APP ?= app
ENV_FILE ?= .env.db-sync

sync-remote-db:
	PATH="$(PG15_BIN):$$PATH" DATABASE_URL="$(DATABASE_URL)" flask --app $(FLASK_APP) sync-remote-db --env-file $(ENV_FILE) --yes

sync-remote-db-confirm:
	PATH="$(PG15_BIN):$$PATH" DATABASE_URL="$(DATABASE_URL)" flask --app $(FLASK_APP) sync-remote-db --env-file $(ENV_FILE)
