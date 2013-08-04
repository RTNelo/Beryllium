#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This module will define some useful object for the blog app.

It will create a mako.TemplateLookup instance for the app.
"""

import tempfile

from mako import lookup

#Prepare the TemplateLookup
template_lookup = lookup.TemplateLookup(
    ['templates/'],  # Path to look up templates.
    module_dictionary=tempfile.mkdtemp(),  # Create a temp directory to
                                           # store compiled templates.
    #TODO: Use options' value.
    filesystem_checkes=True,  # Track the template file, when it
                              # modified, reload it.
    input_encoding='utf-8',  # Encoding of the template files.
)
