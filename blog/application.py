#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The application module define the Application class used by the blog app."""

from tornado import web

import urls  # This module defines the urls.
from options import options


class Application(web.Application):
    def __init__(self):
        """The Application class used by the blog application.
        This application will prepare something for the blog app:
            It will create an alias of urls.urls and use it to initialize.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls

        super(Application, self).__init__(self.app_urls,
                                          debug=options.debug,
                                          cookie_secret=options.cookie_secret,
                                          )
