#!/bin/sh -e

workers=${API_WORKERS:-1}
timeout=${GUNICORN_TIMEOUT:-1200}
worker_type=${GUNICORN_WORKER_TYPE:-"sync"}

echo "Gunicorn settings: Workers: $workers. Timeout: $timeout"
exec gunicorn \
    -n "$(hostname)" \
    --workers "$workers" \
    --reload \
    --error-logfile=/dev/stderr \
    --access-logfile=/dev/stdout \
    --graceful-timeout 1 \
    -b 0.0.0.0:5000 \
    -k "$worker_type" \
    --access-logformat='%(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%(D)s" "%({X-Forwarded-Proto}i)s" "%({X-Forwarded-For}i)s"' \
    --timeout "$timeout" \
    start_app:app
