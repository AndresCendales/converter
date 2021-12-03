#!/bin/sh
chmod 777 -R migrations/
rm -R migrations/
flask db init
flask db migrate
flask db upgrade
python wsgi.py