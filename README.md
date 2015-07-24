## moth: Vulnerable web application

A set of vulnerable scripts which can be used for testing web application
security scanners,  teaching web application security, etc.

This software should **never be used in a production environment**.

This is a rewrite of the [PHP-based moth web application](https://github.com/andresriancho/w3af-moth).

## Usage

```console
$ git clone https://github.com/andresriancho/django-moth.git
$ cd django-moth
$ pip install -r requirements.txt
$ python manage.py runserver
```

Then browse to http://127.0.0.1:8000/ .

## Docker

The easiest way to use `django-moth` is to start a [docker](https://www.docker.com/)
container:

```console
docker run --name moth --rm -p 8000:8000 -p 8001:8001 andresriancho/django-moth
```

Please note that you can build the docker image yourself:

```console
sudo docker build -t andresriancho/django-moth .
```

Or simply [get it from the registry](https://registry.hub.docker.com/u/andresriancho/django-moth/):

```console
sudo docker pull andresriancho/django-moth
```

## Sister repository

[PHP-moth](https://github.com/andresriancho/php-moth) is a sister repository which
holds PHP-specific tests.
