# coding: utf-8

import os
import sys

from simple_wsgi_application import simple_app


def wsgi_to_bytes(s):
    return s.encode()


def run_with_cgi(application):
    # 按照WSGI协议，构建environ内容
    # 1类CGI相关的变量，此脚本就是用于cgi执行，所以前面的web服务器已经将CGI变量封装好，这里直接使用
    environ = {k: v.encode() for k,v in os.environ.items()}
    environ['wsgi.input']           = sys.stdin.buffer
    environ['wsgi.errors']          = sys.stderr
    environ['wsgi.version']         = (1, 0)
    environ['wsgi.multithread']     = False
    environ['wsgi.multiprocess']    = True 
    environ['wsgi.run_once']        = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        # 将内容返回
        out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status: %s\r\n' % status))
            for header in response_headers:
                out.write(wsgi_to_bytes("%s: %s\r\n" % header))
            out.write(wsgi_to_bytes("\r\n"))

        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    raise (exc_info[0], exc_info[1], exc_info[2])
            finally:
                # avoid dangling circular ref
                exc_info = None
        elif headers_set:
            raise AssertionError("Header already set.")

        headers_set[:] = [status, response_headers]
        return write


    # 将上面处理的参数交给应用程序
    result = application(environ, start_response)

    try:
        # 将请求到的结果写回。
        for data in result:
            if data:
                # don't send headers until body appears
                write(data) 
        if not headers_sent:
            # send headers now if body was empty
            write('')
    finally:
        if hasattr(result, 'close'):
            result.close()


if __name__=='__main__':
    run_with_cgi(simple_app)    