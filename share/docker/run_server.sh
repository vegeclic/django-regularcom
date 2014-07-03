#!/bin/sh

echo "Sync + migrate database"
python manage.py syncdb --noinput --migrate
echo "Add fixtures"
python setup_script.py
echo "Launch web server"
nginx
