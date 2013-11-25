#!/usr/bin/env python

# I want to perform the following steps:
#    * Start the Django application as a daemon which will listen both on
#      HTTP and HTTPS.
#
# This is usually used together with w3af/core/controllers/ci/setup_moth.py
#
# This script MUST be runnable from the circle.yml configuration file, in order
# to allow this to run in our CI system, but also in a direct way so that
# developers can start it in their workstations and run the unittests.
#
# The script itself won't daemonize itself, you should do that when calling it.
# 
# When running, the script will print classic "manage.py runserver" output to
# the console, which will help debug any issues. The output looks like this:
#     [20/Nov/2013 23:27:45] "GET /grep/svn_users/ HTTP/1.1" 200 2245
#     [20/Nov/2013 23:27:45] "GET /grep/svn_users/DhHg3l4E.cgi HTTP/1.1" 404 1615
#
# The output from the runserver command will also be written to a temporary file
# which will be made available to the build system as an artifact.
#
import os
import logging
import tempfile
import shlex
import subprocess
import re


LOG_FILE = 'django-moth.log'
CMD_FMT = 'python manage.py runserver --verbosity=3 %s'
MIN_PORT = 8000
MAX_PORT = 16000

EXPECTED_RE = re.compile('Development server is running at http://127\.0\.0\.1:(\d+)/')

# See: w3af.core.controllers.ci.moth
FMT = '/tmp/moth-%s.txt'
HTTP_ADDRESS_FILE = FMT % 'http'
HTTPS_ADDRESS_FILE = FMT % 'https'


def start_django_app(log_directory):
    '''
    Start the django application by running "python manage.py runserver".
    
    Output from the runserver command is stored in a LOG_FILE located in the
    log_directory.
    
    :param log_directory: The location where we should store our logs
    :return: The port in localhost where the application listens for HTTP
             requests
    '''
    log_file = os.path.join(log_directory, LOG_FILE)
    
    for port in xrange(MIN_PORT, MAX_PORT):
        cmd = CMD_FMT % port
        cmd_args = shlex.split(cmd)
    
        p = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            universal_newlines=True
        )
        # TODO! Esperar a que aparezca algun mensaje y parsear la salida
        stdout, stderr = p.communicate_otra_cosa_que_no_espera_al_final()
        
        # Development server is running at http://127.0.0.1:8080/ is what I'm
        # looking for, if the output doesn't contain that, we try with the
        # next port.
        output = stdout + stderr
        mo = EXPECTED_RE.search(output)
        if mo:
            # Success! The server started on the port we tried.
            return port
    
    raise RuntimeError('Failed to start runserver on any port.')


def start_ssl_proxy(http_port):
    '''
    Start an SSL proxy that will listen for HTTPS requests on one port and
    forward them to the Django application which lives in http_port
    
    :param http_port: The TCP/IP port where the Django application listens
    :return: None
    '''
    # TODO: Handle HTTPS
    
    https_port = None
    msg = 'HTTPS development server is running at https://127.0.0.1:%s/'
    print msg % https_port

def write_address_files(http_port, https_port):
    '''
    Since the django application will start on a random port, and we want
    others to know where we are, we just write the address to a fixed file.
    
    :param http_port: The TCP/IP port where the Django application listens
    :param https_port: The TCP/IP SSL port where the Django application listens
    '''
    ADDRESS_FMT = '127.0.0.1:%s'
    file(HTTP_ADDRESS_FILE, 'w').write(ADDRESS_FMT % http_port)
    file(HTTPS_ADDRESS_FILE, 'w').write(ADDRESS_FMT % https_port)
    
if __name__ == '__main__':
    http_port = start_django_app()
    https_port = start_ssl_proxy(http_port)
    write_address_files(http_port, https_port)
    
