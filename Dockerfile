FROM ubuntu:14.04
MAINTAINER Andres Riancho <andres.riancho@gmail.com>

# Avoid warnings when using apt-get
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Upgrade
RUN apt-get update
RUN apt-get upgrade -y

# Install nginx
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update

# Install all
RUN apt-get install -y supervisor joe nginx curl wget ca-certificates
RUN apt-get install -y libssl-dev libxml2-dev libxslt1-dev libmemcached-dev
RUN apt-get install -y git-core python-pip build-essential python-dev python-software-properties

# Build dependencies
RUN pip install --upgrade pip
RUN pip install uwsgi==2.0 lxml==3.3.5 django==1.5.1 django-debug-toolbar==0.9.4 \
                requests==1.2.3 django-crispy-forms==1.3.1 pyOpenSSL==0.13.1 \
                DAWG==0.7.2 pylibmc==1.2.3

# Django moth configuration
RUN useradd ubuntu -d /home/ubuntu
ADD . /home/ubuntu/code/
WORKDIR /home/ubuntu/code/
RUN cp djmoth/wsgi.py wsgi.py
RUN pip install -r requirements/main.txt

RUN python manage.py syncdb --noinput
RUN python manage.py collectstatic --noinput

# Nginx configuration
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/ubuntu/code/docker/nginx.conf /etc/nginx/sites-enabled/

# We want supervisord to run nginx and uwsgi
RUN mkdir -p /var/log/supervisor
RUN ln -s /home/ubuntu/code/docker/supervisord-nginx.conf /etc/supervisor/conf.d/
RUN ln -s /home/ubuntu/code/docker/supervisord-uwsgi.conf /etc/supervisor/conf.d/

# Cleanup to reduce image size
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/pip-build-root
RUN rm -rf /root/.cache/pip/

EXPOSE 8000
EXPOSE 8001

# RUN supervisord with our configuration so that the daemons are started
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
