#!/bin/sh
exec gunicorn --workers "${GUNICORN_WORKERS:-4}" \
               --bind "0.0.0.0:5000" \
               --log-level "${GUNICORN_LOG_LEVEL:-info}" \
               app:app