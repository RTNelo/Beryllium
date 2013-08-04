#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module will parse the config.py and store the options.
"""

from tornado import options as options_module

#Prepare the OptionParser instance.
options = options_module.OptionParser()

#Define the debug option.
des_of_debug = """Blog will enter the debug mode if it is True."""
options.define('debug',
               default=False,
               type=bool,
               help=des_of_debug,
               metavar='BOOL')

#Parse the config.py
options.parse_config_file('config.py')
