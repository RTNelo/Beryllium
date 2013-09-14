#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module will parse the config.py and store the options.
"""

from tornado import options as options_module

#Prepare the OptionParser instance.
options = options_module.OptionParser()

#Define the debug option.
des_of_debug = 'Blog will enter the debug mode if it is True.'
options.define('debug',
               default=False,
               type=bool,
               help=des_of_debug,
               metavar='BOOL',
               group='application',
               )

des_of_host_pattern = 'The host pattern of this blog.'
options.define('host_pattern',
               default='',
               type=str,
               help=des_of_host_pattern,
               metavar='STRING',
               group='application',
               )

des_of_db_address = 'The IP Address of the database server.'
options.define('db_address',
               default='127.0.0.1',
               type=str,
               help=des_of_db_address,
               metavar='STRING',
               group='database',
               )

des_of_db_port = 'The port of the database server.'
options.define('db_port',
               default=3306,
               type=int,
               help=des_of_db_port,
               metavar='INTEGER',
               group='database',
               )

des_of_db_user = 'The user name of the database server.'
options.define('db_user',
               default='root',
               type=str,
               help=des_of_db_user,
               metavar='STRING',
               group='database',
               )

des_of_db_pwd = 'The password of the db_user of the database server.'
options.define('db_pwd',
               default='',
               type=str,
               help=des_of_db_pwd,
               metavar='STRING',
               group='database',
               )

des_of_db_name = 'The name of the database on the database server.'
options.define('db_name',
               default='blog',
               type=str,
               help=des_of_db_name,
               metavar='STRING',
               group='database',
               )

des_of_cookie_secret = 'A long random secret string for secure cookie.'
options.define('cookie_secret',
               default='',
               type=str,
               help=des_of_cookie_secret,
               metavar='LONG_STRING',
               group='application',
               )

#Parse the config.py
options.parse_config_file('blog/config.py')
