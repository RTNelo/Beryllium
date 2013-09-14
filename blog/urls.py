#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The urls module defines the urls used by the blog app.

urls declare the relationship between the handlers and the urls. In another
word, it defines a url should be handled by which handler.
"""

# This module defines the handlers used by the blog app.
import handlers

from tornado import web

urls = [(r'/login/?', handlers.LoginHandler),
        (r'/register/?', handlers.RegisterHandler),
        (r'/user(?:/(\d+))?/?', handlers.UserInfoHandler),
        (r'/article/(\w+)/?', handlers.ArticleHandler),
        #Handle every request out of urls and return a 404 status code.
        (r'.*', web.ErrorHandler, dict(status_code=404)),
        ]
