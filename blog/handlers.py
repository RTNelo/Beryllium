#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The handlers module defines the Handlers used by the blog app."""

from tornado import web

import context


class BaseHandler(web.RequestHandler):
    """The superclass of all Handler which will provide some common methods.

    This class shouldn't be used in the request handle behavior.
    """
    def initialize(self):
        """
        Override to prepare for the handler.
        """
        #It's still empty now.
        pass

    def render_string(self, template_name, **kwargs):
        """
        Override it to provide mako templates support.
        """
        template = context.template_lookup.get_template(template_name)
        return template.render(**kwargs)
