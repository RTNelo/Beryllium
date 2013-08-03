#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The server.py will start a HTTPServer instance listening the 80 port. So you
can use `python server.py` to start you httpserver (and the blog).
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
