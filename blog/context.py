#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This module will define some useful object for the blog app.

Such as the TemplateLookup.
"""

import tempfile

from mako import lookup

import options


#Prepare the TemplateLookup
template_lookup = lookup.TemplateLookup(
    ['templates/'],  # Path to look up templates.
    module_directory=tempfile.mkdtemp(),    # Create a temp directory to store
                                            # compiled templates.
    filesystem_checks=options.options.debug,  # Track the template file, when
                                              # it is modified, reload it.
    input_encoding='utf-8',  # Encoding of the template files.
)
