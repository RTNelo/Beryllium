#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The handlers module defines the Handlers used by the blog app."""
import datetime

from tornado import web

import model


class BaseHandler(web.RequestHandler):
    """The superclass of all Handler which will provide some common methods.

    This class shouldn't be used in the request handle behavior.
    """

    def prepare(self):
        """Prepare for the handle process.

        Will create an alias for self.application.ctx.
        Will check the vistor's secure cookie to get or create a session.
        Will use visitor's IP address to protect the secure cookie from
        being copy.
        """

        #Create an alias for self.application.ctx
        self.ctx = self.application.ctx

        session_id = self.get_secure_cookie('session_id')
        if session_id in self.ctx.session_manager.storage:
            session = self.ctx.session_manager.storage[session_id]
            if session.value.ip != self.request.remote_ip:
                self.create_session_for_visitor()
            else:
                #Refresh (extend the life time of) the session.
                self.ctx.session_manager.refresh_session(session_id)

                self.session = session
        else:
            self.create_session_for_visitor()

    def on_finish(self):
        """Clean up process.

        Store the session.
        """
        key = self.session.key
        self.ctx.session_manager.storage[key] = self.session

    def create_session_for_visitor(self):
        """Create a new session and set the session_id secure cookie.

        Will store the IP address for protecting session_id secure cookie
        from being copy.
        """
        self.session = self.ctx.session_manager.create_session()
        key = self.session.key
        self.session.value.ip = self.request.remote_ip
        self.set_secure_cookie('session_id', key)

    def render_string(self, template_name, **kwargs):
        """Override it to provide mako templates support."""
        template = self.ctx.template_lookup.get_template(template_name)
        namespace = self.get_template_namespace()
        namespace.update(kwargs)
        return template.render(**namespace)

    def get_template_namespace(self):
        """Override to provide some common variables to template."""
        return dict(request=self.request,
                    current_user=self.get_current_user()
                    )

    def get_current_user(self):
        """Override to determine the current user."""
        if 'user' in self.session.value:
            return self.session.value.user
        else:
            return None

    def set_current_user(self, user):
        """Set the current user.

        args:
            user(model.User):
                The current user you want to set.
        """
        self.session.value.user = user


class RegisterHandler(BaseHandler):
    """Handle register request."""
    @web.addslash
    def get(self):
        """Render the register template."""
        self.render('register.tpl')

    def post(self):
        """Check the request's email and nickname and create a User.

        The request must have email, password, nickname argument and the email
        and nickname must be unique in the database. Then create a user object
        for it and commit to the database.
        """
        try:
            email = self.get_argument('email')
            password = self.get_argument('password')
            nickname = self.get_argument('nickname')
        except (web.MissingArgumentError, ValueError):
            self.render('register.failed.tpl')
            return
        if (not model.User.have_user(email) and
                not model.User.have_user(nickname, is_nickname=True)):
            user = model.User(email,
                              password,
                              nickname,
                              self.request.remote_ip)
            user.track()
            model.commit()
            self.set_current_user(user)
            self.render('register.successful.tpl')
        else:
            self.render('register.failed.tpl')


class LoginHandler(BaseHandler):
    """Handler handle login request."""
    @web.addslash
    def get(self):
        """When receive a get request of login, render the login template."""
        self.render('login.tpl')

    def post(self):
        """When receive a post request of login check it and display result.

        If email and password is not None and a user can meet them, set the
        current user and display a successful news. Or display a failed news.
        """
        try:
            email = self.get_argument('email')
            password = self.get_argument('password')
        except web.MissingArgumentError:
            self.render('login.failed.tpl')
            return
        user = model.User.get_user_by_email_and_password(email, password)
        if user is None:
            self.render('login.failed.tpl')
        else:
            self.set_current_user(user)
            self.render('login.successful.tpl')

            #Update user's information.
            user.last_login_time = datetime.datetime.utcnow()
            user.last_login_ip = self.request.remote_ip
            model.commit()


class UserInfoHandler(BaseHandler):
    """Handler of displaying user's information."""
    @web.addslash
    def get(self, user_id=None):
        """Render the user_info template.

        If user_id is not None, get_user by the user id then set template args
        to the user if the get_user return is not None, else write 404 error. if
        the user_id is None, and get_current_user is not None, just render the
        user_info template for displaying current user's information, if
        get_current_user is None, write 404 error.
        """
        if user_id is not None:
            user = model.User.get_user(int(user_id))
            if user is not None:
                self.render('user_info.tpl', user=user)
            else:
                self.write_error(404)
        elif self.get_current_user() is not None:
            self.render('user_info.tpl', user=self.get_current_user())
        else:
            self.write_error(404)
