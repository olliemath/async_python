#!/bin/sh -e

worker_type=${GUNICORN_WORKER_TYPE:-"sync"}

echo "Gunicorn workers: $workers."
exec gunicorn -n "$(hostname)" -w 1 -k "$worker_type" -b 0.0.0.0:5000 --reload gunicorn_entrypoint:app
