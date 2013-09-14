#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The server.py will start a HTTPServer instance listening the 80 port. So you
can use `python server.py` to start you httpserver (and the blog).

It will create a context object containing a Cron Runer and a Session Manager for
the application. If the script exit after the context being created, it will clean
the context (stop the Cron Runner) automatically.
"""

import datetime

from tornado import httpserver
from tornado import ioloop
from tornado import util

import cron
import session

from blog import application


def prepare():
    """Prepare the context object containing SessionManager and CronRunner."""
    ctx = util.ObjectDict()

    #Prepare the SessionManager.
    ctx.session_manager = session.SessionManager()
    #Create and start a cron task runner.
    ctx.cron_runner = cron.Cron()
    ctx.cron_runner.start()

    return ctx


def clean(ctx):
    """Clean up the context. It will stop and close the cron_runner."""
    ctx.cron_runner.stop()
    ctx.cron_runner.join()
    ctx.cron_runner.close()


def main():
    """Main fuction which will start a HTTPServer listening the 80 port

    It also clean context finally. If you use the blog without start the main
    fuction, please invoke the clean function yourself.
    """
    ctx = None
    try:
        ctx = prepare()
        #Clean expired session once an hour.
        ctx.cron_runner.add_timer_task(ctx.session_manager.clean_expired_session,
                                       datetime.timedelta(hours=1))

        http_server = httpserver.HTTPServer(application.Application(ctx))
        http_server.listen(80)

        print 'HTTPServer listening 80 will start now.'
        ioloop.IOLoop.instance().start()
    finally:
        if ctx is not None:
            clean(ctx)

if __name__ == '__main__':
    main()
