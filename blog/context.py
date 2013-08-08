#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""This module defines some useful object for the blog app."""

import tempfile

from mako import lookup

import options
import session
import cron


#Prepare the TemplateLookup
template_lookup = lookup.TemplateLookup(
    directories=['blog/templates'],  # Path to look up templates.
    module_directory=tempfile.mkdtemp(),    # Create a temp directory to store
                                            # compiled templates.
    filesystem_checks=options.options.debug,  # Track the template file, when
                                              # it is modified, reload it.
    input_encoding='utf-8',  # Encoding of the template files.
)

#Prepare the SessionManager.
session_manager = session.SessionManager()

#Create and start a cron task runner.
cron_runner = cron.Cron()
cron_runner.start()


def clean():
    """Clean up the context. It will stop and close the cron_runner."""
    cron_runner.stop()
    cron_runner.join()
    cron_runner.close()
