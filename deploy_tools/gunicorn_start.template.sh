#!/bin/bash

cd /home/ubuntu/sites/DOMAIN
. /home/ubuntu/sites/DOMAIN/virtualenv/bin/activate
python3.6 manage.py collectstatic --noinput
gunicorn superlists.wsgi:application -b unix:/tmp/DOMAIN.socket
