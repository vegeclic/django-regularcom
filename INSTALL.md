Installation
============

(1) Start by renaming the file regularcom/settings.py-dist to
regularcom/settings.py and configure the database specific variables.

(2) Then create the whole database in using the command line:
./manage.py syncdb

(3) You can use now the command line: ./manage.py runserver in order
    to start an instance and go right now to http://localhost:8000
    with your prefered browser.

(more) If you want to use celery tasks, you can use as a backend
       rabbitmq:

       (a) start an instance of rabbitmq with the command line: sudo
       rabbitmq-server

       (b) start a worker (+ celery beat instance) with the commad
       line: ./manage.py celery worker -B
