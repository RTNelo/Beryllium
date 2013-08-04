#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The application module define the Application class used by the blog app.

Application will use the urls in the urls module to initialize it self.
"""
from tornado import web

import urls  # This module defines the urls.


class Application(web.Application):
    def __init__(self):
        """The Application class used by the blog application. It will prepare
        something for the blog app.
        Now it just create an alias of urls.urls and use it to initialize.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls

        super(Application, self).__init__(self.app_urls)
