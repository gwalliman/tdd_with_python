#!/bin/bash

cd /home/ubuntu/sites/DOMAIN
. /home/ubuntu/sites/DOMAIN/bin/activate
python3.6 manage.py collectstatic --noinput
gunicorn settings.config.wsgi:application -b unix:/tmp/DOMAIN.socket
