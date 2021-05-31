# coding: utf-8

import os
import sys

from simple_wsgi_app import simple_app

def wsgi_to_bytes(s):
    return s.encode()

def run_with_cgi(application):
    environ = os.environ.items()
    environ['wsgi.input'] = sys.stdin.buffer
    environ['wsgi.errors'] = sys.stderr
    