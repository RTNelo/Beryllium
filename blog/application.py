#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The application module define the Application class used by the blog app.

Application will use the urls in the urls module to initialize it self. Then
prepare the context object.
"""
from tornado import web

import urls  # This module defines the urls.
import options
from context import context


class Application(web.Application):
    def __init__(self):
        """The Application class used by the blog application. It will prepare
        something for the blog app.
        It will create an alias of urls.urls and use it to initialize. Then
        prepare the context object.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls
        #Prepare the context object in the context module.
        context.prepare()

        super(Application, self).__init__(self.app_urls,
                                          debug=options.options.debug
                                          )
