#!/bin/bash

exec gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0 mipres_app.wsgi:app
"$@"
