#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple cron system based on tornado.ioloop.IOLoop."""


import threading

from tornado import ioloop


class Cron(threading.Thread):
    """A simple Cron runner.

    Usage:
        Create a new Cron and start it. Then use add_timer_task to add task.
        Then use stop to send stop signal to the cron. Then use is_alive or
        join to check.
    """
    def __init__(self):
        """Will create a new IOLoop."""
        self.ioloop = ioloop.IOLoop()
        super(Cron, self).__init__()

    def run(self):
        """The main function of the thread. Will only start the ioloop."""
        self.ioloop.start()

    def add_timer_task(self, task, interval):
        """Add a task which will be excute time by time with a interval.

        The task will be started interval time after invoking this method.
        args:
            task(callable): task to run.
            interval(datetime.timedelta): how long the interval is.
        """
        task = _Task(task, interval, self.ioloop)
        task.add_callback()

    def stop(self):
        """Send a stop signal to the cron.

        The cron may still running after you use stop method. So use is_alive
        or join to make sure that the cron was stop.
        """
        self.ioloop.stop()

    def close(self):
        """Release source used by the ioloop of the cron."""
        self.ioloop.close()


class _Task(object):
    """A private class for Cron

    Cron will use a task(callable), a interval and Cron's ioloop to create a
    _Task, and use _Task.add_callback() to add the task to the ioloop. Every
    time the _Task is call, the _Task will run the add_callback to add itself
    to the ioloop for the next time.
    """
    def __init__(self, callable, interval, ioloop):
        """Create a _Task which will be excuted by ioloop with a interval.

        args:
            callable(callable);
            interval(datetime.timedelta);
            ioloop(tornado.ioloop.IOLoop).
        """
        self.callable = callable
        self.interval = interval
        self.ioloop = ioloop

    def __call__(self):
        """Call the callable and add callback to the ioloop."""
        self.callable()
        self.add_callback()

    def add_callback(self):
        """Add callback(the _Task) to the ioloop."""
        self.ioloop.add_callback(self.ioloop.add_timeout, self.interval, self)
