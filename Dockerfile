FROM canercandan/nginx_passenger-base
MAINTAINER Caner Candan <caner@candan.fr>

# convert and install fandjango
WORKDIR /root
RUN git clone https://github.com/jgorset/fandjango.git
WORKDIR /root/fandjango
RUN pip install -r requirements.txt
RUN 2to3-3.4 -w .
RUN python setup.py install

# install our code
WORKDIR /app
ADD . /app

# install all dependencies
RUN pip install -r requirements.txt

# install static files
RUN python manage.py collectstatic --noinput

# sync database
ONBUILD RUN python manage.py syncdb --noinput --migrate

# run
EXPOSE 80
CMD ["nginx"]
