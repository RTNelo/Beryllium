#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The handlers module defines the Handlers used by the blog app.

All handlers defined in this module is the subclass of the BaseHandler. The
BaseHandler is extended from tornado.RequestHandler.

"""
from tornado import web


class BaseHandler(web.RequestHandler):
    """The superclass of all the other handlers defined in this module. defines
    some common methods.

    It shouldn't be used in the request handle.
    """
    #The BaseHandler is empty now.
    pass
