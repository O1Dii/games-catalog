#!/usr/bin/env bash

python manage.py migrate
python manage.py sync_igdb 1000
uwsgi --socket :8001 --module itechart_project.wsgi