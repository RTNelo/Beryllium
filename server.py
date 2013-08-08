#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The server.py will start a HTTPServer instance listening the 80 port. So you
can use `python server.py` to start you httpserver (and the blog).
"""

from tornado import httpserver
from tornado import ioloop

from blog import application
from blog import context


def clean():
    context.clean()


def main():
    """Main fuction which will start a HTTPServer listening the 80 port

    It also clean context finally. If you use the blog without start the main
    fuction, please invoke the clean function yourself.
    """
    try:
        http_server = httpserver.HTTPServer(application.Application())
        http_server.listen(80)
        print 'HTTPServer listening 80 will start now.'
        ioloop.IOLoop.instance().start()
    finally:
        clean()

if __name__ == '__main__':
    main()
