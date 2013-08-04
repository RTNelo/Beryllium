#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This module will define some useful object for the blog app.

It will create a mako.TemplateLookup instance for the app.
"""

import tempfile

from mako import lookup

from tornado import util

import options


class Context(util.ObjectDict):
    def prepare(self):
        """Application should invoke this function before use the context."""
        #Prepare the TemplateLookup
        self.template_lookup = lookup.TemplateLookup(
            ['templates/'],  # Path to look up templates.
            module_dictionary=tempfile.mkdtemp(),  # Create a temp directory to
                                                   # store compiled templates.
            filesystem_checkes=options.options.debug,  # Track the template
                                                       # file, when it is
                                                       # modified, reload it.
            input_encoding='utf-8',  # Encoding of the template files.
        )

context = Context()
