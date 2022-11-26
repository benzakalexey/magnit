#!/usr/bin/env bash
set -e
if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi
if [ -z "$API_PORT" ]; then
  API_PORT=8082
fi
# shellcheck disable=SC2089
GUNICORN_CMD_ARGS="--bind=0.0.0.0:$API_PORT --workers=1 --log-level $API_LOG_LEVEL --log-file - --forwarded-allow-ip '*' --proxy-allow-from '*' --timeout 300"
# shellcheck disable=SC2090
export GUNICORN_CMD_ARGS

gunicorn magnit.composites.api:app
