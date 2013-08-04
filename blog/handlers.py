#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The handlers module defines the Handlers used by the blog app.

All handlers defined in this module is the subclass of the BaseHandler. The
BaseHandler is extended from tornado.RequestHandler.

"""
from tornado import web

from context import context


class BaseHandler(web.RequestHandler):
    """The superclass of all the other handlers defined in this module. defines
    some common methods.

    It shouldn't be used in the request handle.
    """
    def initialize(self):
        """
        Override to prepare for the handler.
        """
        #It still empty now.
        pass

    def render_string(self, template_name, **kwargs):
        """
        Override to provide mako templates support.
        """
        template = context.template_lookup.get_template(template_name)
        return template.render(**kwargs)
