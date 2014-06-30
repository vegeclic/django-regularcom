FROM canercandan/nginx_passenger-base
MAINTAINER Caner Candan <caner@candan.fr>

# convert and install fandjango
WORKDIR /root
RUN git clone https://github.com/jgorset/fandjango.git
WORKDIR /root/fandjango
RUN pip install -r requirements.txt
RUN 2to3-3.4 -w .
RUN python setup.py install

WORKDIR /app

# install all dependencies
ADD requirements.txt /app/
RUN pip install -r requirements.txt

# install our code
ADD . /app
RUN chown -R www-data:www-data /app

# install static files
RUN python manage.py collectstatic --noinput

# compile translation messages
RUN python manage.py compilemessages

# run
EXPOSE 80
CMD ["sh", "run_server.sh"]
# CMD ["nginx"]
