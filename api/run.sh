#!/bin/sh -e

interpreter=${INTERPRETER:-"pypy3"}
worker_type=${GUNICORN_WORKER_TYPE:-"sync"}
echo "Gunicorn workers: $worker_type."

echo "Running migrations"
$interpreter migrate.py || exit 1

echo "Starting app with $INTERPRETER"
exec $INTERPRETER -m gunicorn.app.wsgiapp -w 1 -k "$worker_type" -b 0.0.0.0:5000 --reload gunicorn_entrypoint:app
