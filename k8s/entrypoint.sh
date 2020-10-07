#!/bin/bash

exec gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 mipres_app.wsgi:app
"$@"
