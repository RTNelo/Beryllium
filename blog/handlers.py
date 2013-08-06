#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The handlers module defines the Handlers used by the blog app."""

from tornado import web

import context


class BaseHandler(web.RequestHandler):
    """The superclass of all Handler which will provide some common methods.

    This class shouldn't be used in the request handle behavior.
    """
    def prepare(self):
        """Prepare for the handle process.

        Will check the vistor's secure cookie to get or create a session.
        Will use visitor's IP address to protect the secure cookie from
        being copy.
        """
        session_id = self.get_secure_cookie('session_id')
        if session_id in context.session_manager.storage:
            session = context.session_manager.storage[session_id]
            if session.value.ip != self.request.remote_ip:
                self.create_session_for_visitor()
        else:
            self.create_session_for_visitor()

    def finish(self):
        """Clean up process.

        Store the session.
        """
        key = self.session.value.key
        context.session_manager.storage[key] = self.session

    def create_session_for_visitor(self):
        """Create a new session and set the session_id secure cookie.

        Will store the IP address for protecting session_id secure cookie
        from being copy.
        """
        key, self.session = context.session_manager.create_session()
        self.session.value.ip = self.request.remote_ip
        self.set_secure_cookie('session_id', key)

    def render_string(self, template_name, **kwargs):
        """
        Override it to provide mako templates support.
        """
        template = context.template_lookup.get_template(template_name)
        return template.render(**kwargs)
