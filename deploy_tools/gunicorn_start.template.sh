#!/bin/bash

cd <PATH/TO/DJANGO/ROOT>
. <PATH/TO/DJANGO/ROOT>/bin/activate
python3.6 manage.py collectstatic --noinput
gunicorn settings.config.wsgi:application -b unix:/tmp/<SOCKET_NAME>.socket
