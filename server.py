#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Beryllium is a simple blog application. And the Be-5 version is the lightest
one.

The server.py will start a HTTPServer instance and make it listen the 80 port.
So you can use `python server.py` to start you httpserver (and the blog).

The blog package is the blog application itself.

The blog.application defines the the Application class used by the blog
application.

The blog.urls defines the relationship between the handlers and the urls.

The blog.handlers defines the handlers used in the app.
"""

from tornado import httpserver
from tornado import ioloop

from blog import application


def main():
    """Main fuction which will create a HTTPServer listening the 80 port And
    start it."""
    http_server = httpserver.HTTPServer(application.Application)
    http_server.listen(80)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
