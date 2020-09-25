#!/bin/bash

exec gunicorn mipres_app.wsgi:app \
    --pid mipres-api.pid \
    --name docker_mipres_app \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=debug \
    --timeout 60
"$@"