#!/bin/sh
#flask db init
#flask db migrate
flask db upgrade

gunicorn -c ./config/prod/gunicorn.config.py wsgi:app