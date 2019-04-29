#!/bin/bash

cd /home/ubuntu/sites/DOMAIN
set -a; . /home/ubuntu/sites/DOMAIN/.env; set +a;
. /home/ubuntu/sites/DOMAIN/virtualenv/bin/activate
python3.6 manage.py collectstatic --noinput
gunicorn superlists.wsgi:application -b unix:/tmp/DOMAIN.socket
