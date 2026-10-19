#!/usr/bin/env bash
# Run Maestro flows against staging with the synthetic account.
#   tools/maestro/e2e.sh .maestro/flows/            # a directory
#   tools/maestro/e2e.sh .maestro/flows/01_x.yaml   # one flow
# Maestro 2.x ignores exported shell variables, so credentials are passed with -e.
set -euo pipefail
ENV_FILE="${ENV_FILE:-.maestro/.env.local}"
PATTERN="${SYNTHETIC_EMAIL_PATTERN:-+test@}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "No $ENV_FILE. Copy tools/maestro/.env.local.example there and fill it in (synthetic account)." >&2
  exit 1
fi
set -a; source "$ENV_FILE"; set +a
if [[ -z "${APP_EMAIL:-}" || -z "${APP_PASSWORD:-}" ]]; then
  echo "APP_EMAIL and APP_PASSWORD must be set in $ENV_FILE." >&2
  exit 1
fi
if [[ "$APP_EMAIL" != *"$PATTERN"* ]]; then
  echo "Refusing: APP_EMAIL is not a synthetic account (must contain '$PATTERN'). Staging only." >&2
  exit 1
fi
if [[ $# -eq 0 ]]; then
  echo "usage: $0 <flow.yaml|dir> [more maestro test args]" >&2
  exit 2
fi
exec maestro test -e APP_EMAIL="$APP_EMAIL" -e APP_PASSWORD="$APP_PASSWORD" "$@"
