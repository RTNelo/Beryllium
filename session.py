#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import string

import tornado.util


class SessionStorage(dict):
    """The class store sessions."""
    pass


class Session(object):
    """The session. Store a value and a expire_time."""
    def __init__(self, key, expire_time, value=None):
        """
        args:
            expire_time(datetime.datetime):
                When the session expire. UTC time.
            key(str):
                The key of the session in it's SessionStorage.
            value(dict, default=None):
                Use value to init a ObjectDict as self.value. If it is None,
                use an empty dict.
        """
        self.key = key
        self.expire_time = expire_time
        self.value = tornado.util.ObjectDict(value or dict())

    def expired(self):
        """If this session expired?
        return(bool):
            If the session expired?
        """
        return datetime.datetime.utcnow() > self.expire_time

    def reset_expire_time(self, expire_time):
        """Reset the Session expire time.

        args:
            expire(datetime.datetime):
                When the session should be expired.
        """
        self.expire_time = expire_time


class SessionManager(object):
    """The object manage session.

    Use a SessionManager's storage attribute to visit a session.
    """
    def __init__(self,
                 default_expire=datetime.timedelta(hours=1),
                 storage=SessionStorage,
                 ):
        """
        args:
            default_expire(datetime.timedelta):
                The default life time of a session. self.create_session will use
                this as the default life time as a new session.
            storage(type):
                The storage class of the SessionManager. Must look like a
                tornado.util.ObjectDict.
        """
        self.default_expire = default_expire
        self.storage = SessionStorage()

    def create_session(self, value=None, expire=None):
        """Create a new Session stored in self.storage.

        Will use str(datetime.datetime.utcnow()) + [a random string consists
        of 10 ascii letters] as storage's key. It will guarantee the key is
        unique.
        args:
            value(dict, default=None):
                The value of the new session. If it is None, use an empty dict.
            expire(datetime.timedelta, default=None):
                The life time of the new session. If it is Nonw, will use The
                manager's default_expire.
        return((str, Session)):
            A tuple like (key, Created session)
        """
        value = value or dict()
        expire = expire or self.default_expire

        create_time = datetime.datetime.utcnow()

        #Get a new key.
        while True:
            key = ''.join([str(create_time)] +
                          random.sample(string.ascii_letters, 10))
            if key not in self.storage:
                break
        session = Session(key, create_time + expire, value)
        self.storage[key] = session
        return session

    def refresh_session(self, key, expire=None):
        """Reset the expire_time of session with key to utcnow + expire.

        args:
            expire(datetime.timedelta, default=None):
                The life time of the session after refresh. Will use the
                default_expire of SessionManager if it is None.
        raise:
            KeyError: if there is no session with the key. Raise a KeyError.
        """
        if key not in self.storage:
            raise KeyError(('SessionStorage have'
                            'no session with key {0}').format(key))
        else:
            expire = expire or self.default_expire
            now = datetime.datetime.utcnow()
            self.storage[key].reset_expire_time(now + expire)

    def del_session(self, key):
        """Delete a session.
        args:
            key(str): the key of the session you want to delete.
        """
        del self.storage[key]

    def clean_expired_session(self):
        """Delete all expire session in the storage."""
        for key, session in self.storage.copy().iteritems():
            if session.expired():
                del self.storage[key]
