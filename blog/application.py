#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The application module define the Application class used by the blog app.

Application will use the urls in the urls module to initialize it self. And it
will define a debug option used by the application itself. Then prepare the
context object.
"""
from tornado import web

import urls  # This module defines the urls.
import options
from context import context

#Define the debug option.
des_of_debug = """Blog will enter the debug mode if it is True."""
options.options.define('debug',
                       default=False,
                       type=bool,
                       help=des_of_debug,
                       metavar='BOOL')


class Application(web.Application):
    def __init__(self):
        """The Application class used by the blog application. It will prepare
        something for the blog app.
        It will create an alias of urls.urls and use it to initialize. And
        parse the config file, prepare the context object.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls
        #Parse the config file.
        options.options.parse_config_file('config.py')
        #Prepare the context object in the context module.
        context.prepare()

        super(Application, self).__init__(self.app_urls,
                                          debug=options.options.debug
                                          )
