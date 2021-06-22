# coding: utf-8

def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return [b'Hello World! Mr. Django. \n']