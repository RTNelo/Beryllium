#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""This module defines some useful object for the blog app."""

import tempfile

from mako import lookup
from tornado import util

import options


context = util.ObjectDict()

#Prepare the TemplateLookup
context.template_lookup = lookup.TemplateLookup(
    directories=['blog/templates'],  # Path to look up templates.
    module_directory=tempfile.mkdtemp(),    # Create a temp directory to store
                                            # compiled templates.
    filesystem_checks=options.options.debug,  # Track the template file, when
                                              # it is modified, reload it.
    input_encoding='utf-8',  # Encoding of the template files.
)
