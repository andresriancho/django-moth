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
import sys
import argparse
import select
import shlex
import subprocess
import threading
import re

LOG_FILE = 'django-moth.log'
SSL_LOG_FILE = 'django-moth-ssl.log'

CMD_FMT = '%s manage.py trunserver %s'
SSL_CMD_FMT = '%s manage.py trunserver %s --ssl-priv-key=ssl/privkey.pem'\
              ' --ssl-cert=ssl/cacert.pem'
MIN_PORT = 8000
MAX_PORT = 16000

EXPECTED_RE = re.compile('Site starting on (\d+)')
SSL_EXPECTED_RE = re.compile('Site \(TLS\) starting on (\d+)')

# See: w3af.core.controllers.ci.moth
FMT = '/tmp/moth-%s.txt'
HTTP_ADDRESS_FILE = FMT % 'http'
HTTPS_ADDRESS_FILE = FMT % 'https'


def start_django_app_http(log_directory, python):
    return _start_django_app(log_directory, python, CMD_FMT,
                             EXPECTED_RE, LOG_FILE)


def start_django_app_https(log_directory, python):
    return _start_django_app(log_directory, python, SSL_CMD_FMT,
                             SSL_EXPECTED_RE, SSL_LOG_FILE)


def _start_django_app(log_directory, python, cmd_fmt, expected_re, log_file):
    """
    Start the django application by running "python manage.py runserver".
    
    Output from the runserver command is stored in a LOG_FILE located in the
    log_directory.
    
    :param log_directory: The location where we should store our logs
    :param python: The path to the python executable, useful for supporting
                   running this inside a virtual environment.
    :param cmd_fmt: The command format to use to start the server
    :param expected_re: A regular expression object that's used to match the
                        successful start of trunserver
    :return: The port in localhost where the application listens for HTTP
             requests
    """
    log_file_path = os.path.join(log_directory, log_file)
    log_file = file(log_file_path, 'w')
    
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    
    for port in xrange(MIN_PORT, MAX_PORT):
        cmd = cmd_fmt % (python, port)
        #cmd = '%s | tee %s' % (cmd, log_file)
        cmd_args = shlex.split(cmd)
        
        p = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            universal_newlines=True,
            env=env,
            cwd=os.path.dirname(os.path.realpath(__file__)),
        )
        
        # pylint: disable=E1101
        # Read output while the process is alive
        line = ''
        while p.poll() is None:
            reads, _, _ = select.select([p.stdout, p.stderr], [], [], 1)
            for r in reads:
                out = r.read(1)
                line += out
                log_file.write(out)
                
                if out == '\n':
                    # Development server is running at http://127.0.0.1:8080/
                    # is what I'm looking for, if the output doesn't contain 
                    # that, we try with the next port.
                    if expected_re.search(line):
                        # Success! The server started on the port we tried.
                        msg = 'Daemon is running at 127.0.0.1:%s'
                        print msg % port
                        
                        monitor_thread = threading.Thread(target=log_monitor,
                                                  args=(p, log_file))
                        monitor_thread.start()

                        return p, monitor_thread, port
                    elif 'Address already in use' in line:
                        # Die, die, dieeee!
                        p.kill()
                    else:
                        line = ''
    
    raise RuntimeError('Failed to start runserver on any port.')


def log_monitor(process, log_file):
    """
    :param process: The process we want to read output from
    :param log_file: The file where output should be written
    """
    while process.poll() is None:
        reads, _, _ = select.select([process.stdout, process.stderr], [], [], 1)
        for r in reads:
            log_file.write(r.read(1))
        
        log_file.flush()


def write_address_files(http_port, https_port):
    """
    Since the django application will start on a random port, and we want
    others to know where we are, we just write the address to a fixed file.
    
    :param http_port: The TCP/IP port where the Django application listens
    :param https_port: The TCP/IP SSL port where the Django application listens
    """
    print 'Writing address files ...',
    
    ADDRESS_FMT = '127.0.0.1:%s'
    file(HTTP_ADDRESS_FILE, 'w').write(ADDRESS_FMT % http_port)
    file(HTTPS_ADDRESS_FILE, 'w').write(ADDRESS_FMT % https_port)
    
    print ' done!' 


def parse_args():
    parser = argparse.ArgumentParser(description='Start django-moth daemons.')
    
    parser.add_argument('--log-directory', help='Where to store log files.',
                        required=False, dest='log_directory', default='/tmp/')

    namespace = parser.parse_args()
    
    return namespace.log_directory

if __name__ == '__main__':
    log_directory = parse_args()
    python = sys.executable

    print('Saving logs to %s' % log_directory)
    
    p1, monitor_thread, http_port = start_django_app_http(log_directory, python)
    p2, monitor_thread, https_port = start_django_app_https(log_directory, python)
    write_address_files(http_port, https_port)
    
    try:
        # pylint: disable=E1101
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        print('')
        print('Ctrl+C. Exit.')
    else:
        print('Exit.')
