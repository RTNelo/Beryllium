#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The urls module defines the urls used by the blog app.

urls declare the relationship between the handlers and the urls. In another
word, it defines a url should be handled by which handler.
"""

# This module defines the handlers used by the blog app.
import handlers

from tornado import web
from tornado.web import url

urls = [url(r'/login/?', handlers.LoginHandler, name='login'),
        url(r'/logout/?', handlers.LogoutHandler, name='logout'),
        url(r'/register/?', handlers.RegisterHandler, name='register'),
        url(r'/user/?', handlers.UserInfoHandler, name='self'),
        url(r'/user/(\d+)/?', handlers.UserInfoHandler, name='user'),
        url(r'/article/(\w+?)/?', handlers.ArticleHandler, name='article'),
        url(r'/submit/article/?', handlers.ArticleSubmitHandler,
            name='submit_article'),
        url(r'/submit/comment/?', handlers.CommentSubmitHandler,
            name='submit_comment'),
        #Handle every request out of urls and return a 404 status code.
        url(r'.*', web.ErrorHandler, dict(status_code=404)),
        ]
