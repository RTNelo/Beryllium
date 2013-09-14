#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The application module define the Application class used by the blog app."""

from tornado import web

import urls  # This module defines the urls.
import context as ctx_module

from options import options


class Application(web.Application):
    def __init__(self, context):
        """The Application class used by the blog application.

        This application will prepare something for the blog app:
            It will create an alias of urls.urls and use it to initialize.
            Update the context by the context module's context.
        args:
            context(tornado.util.ObjectDict): containing something the application
                need, created by the server.py.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls

        context.update(ctx_module.context)
        self.ctx = context

        super(Application, self).__init__(debug=options.debug,
                                          cookie_secret=options.cookie_secret,
                                          login_url='/login/',
                                          )

        self.add_handlers(options.host_pattern, self.app_urls)
