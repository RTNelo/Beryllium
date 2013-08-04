#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Beryllium is a simple blog application. And the Be-5 version is the lightest
one.

The blog package is the blog application itself.

The blog.application defines the the Application class used by the blog
application.

The blog.urls defines the relationship between the handlers and the urls.

The blog.handlers defines the handlers used in the app.

The blog.context defines some useful instance used by the app, such as
template lookup and database instance.

The blog.options will define the options and  parse the config.py.

The blog.model will define the datamodel used by the app.
"""
import application
import urls
import handlers
import context
import options
import model

__all__ = ['application',
           'urls',
           'handlers',
           'context',
           'options',
           'model',
           ]
