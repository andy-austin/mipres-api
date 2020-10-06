#!/bin/bash

exec gunicorn --worker-class eventlet mipres_app.wsgi:app \
    --pid mipres-api.pid \
    --name docker_mipres_app \
    --bind 0.0.0.0:80 \
    --workers 5 \
    --log-level=debug \
    --timeout 60
"$@"
