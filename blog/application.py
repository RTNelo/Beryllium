#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The application module define the Application class used by the blog app.

Application will use the urls in the urls module to initialize it self.
"""
import tempfile

from tornado import web
from mako import lookup

import urls  # This module defines the urls.


class Application(web.Application):
    def __init__(self):
        """The Application class used by the blog application. It will prepare
        something for the blog app.
        Now it just create an alias of urls.urls and use it to initialize.
        """
        #Make an alias of the urls.
        self.app_urls = urls.urls

        #Prepare the TemplateLookup
        self.template_lookup = lookup.TemplateLookup(
            ['templates/'],  # Path to look up templates.
            module_dictionary=tempfile.mkdtemp(),  # Create a temp directory to
                                                   # store compiled templates.
            #TODO: Use options' value.
            filesystem_checkes=True,  # Track the template file, when it
                                      # modified, reload it.
            input_encoding='utf-8',  # Encoding of the template files.
        )

        super(Application, self).__init__(self.app_urls)
