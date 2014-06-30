#!/bin/sh

python manage.py syncdb --noinput --migrate
python setup_script.py
nginx
