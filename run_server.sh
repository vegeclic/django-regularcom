#!/bin/sh

python manage.py syncdb --noinput --migrate
python setup_script.py
#memcached -u memcache -d
nginx
