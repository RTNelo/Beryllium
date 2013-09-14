#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides some simple and common function and class."""

import hashlib
import datetime
import functools
import urllib

import markdown2


def hash_repeat(raw, salt_pre='', salt_suf='', time=3):
    """This function will multi-hash a string and return the hash value.

    args:
        raw(str):
            The string you want to get hash value.
        salt_pre(str):
            The salt added before the raw.
        salt_suf(str):
            The salt added after the raw.
        time(int):
            How many times hash process would you like.
    return(str):
        The hash value of raw.
    """
    res = raw
    for i in xrange(time):
        res = hashlib.sha256(''.join((salt_pre, res, salt_suf))).hexdigest()
    return res


def remove_microsecond(time):
    """Return a new datetime object from arg time that microsecond is 0.

    args:
        time(datetime.datetime):
            Which datetime object you want to remove microsecond.
    return(datetime.datetime):
        A new datetime object same as arg time but microsecond is 0.
    """
    delta = datetime.timedelta(microseconds=time.microsecond)
    return time - delta


def content_convert(raw, converter=markdown2.markdown):
    """Convert the markdown content to content for visitor.
    args:
        raw(str):
            Raw content need convertint.
        converter(callable):
            content_convert will return the result of converter(raw).
    return(str):
        The content value. Encoding is UTF-8.
    """
    return converter(raw).encode('utf-8')


def apply_args_to_converter(converter, *args, **kwargs):
    """Apply args to a converter (callable).

    args:
        converter(callable):
            The converter you want to apply args on.
        *args:
            The args you want to apply.
        **kwargs:
            The key-value args you want to apply.
    return(functools.partial):
        A callable that equal to converter([args you provide], *args,
        **kwargs).
    """
    return functools.partial(converter, args, kwargs)


def apply_args_to_md_converter(*args, **kwargs):
    """Same as apply_args_to_converter, but converter is markdown2.markdown"""
    return apply_args_to_converter(markdown2.markdown, *args, **args)


def create_reverse_url(app, host_pattern):
    """Create a function can return reverse_url (with host_pattern) of app.

    You can use the func.app to access the application instance.
    You also can access the host_pattern processed by this function.
    """
    if host_pattern[-1] != '/':
        host_pattern = ''.join((host_pattern, '/'))
    type_of_host, rest = urllib.splittype(host_pattern)
    #If host_pattern give a type(\w://), the rest will have //
    if rest[:2] == '//':
        rest = rest[2:]

    def func(name, type=None, *args):
        """Return the reversed url.

        It will get the type of host_pattern. If the type param is not None, it
        will use this param as the reversed url's type, or it will try to use
        the type of the host_pattern. If host_pattern didn't give a type, it
        will use http as the type.
        """
        type = type or type_of_host or 'http'
        reverse_url = app.reverse_url(name, *args)[1:]  # remove the '/' ahead.
        res = urllib.basejoin('{0}://{1}'.format(type, rest), reverse_url)
        return res

    func.app = app
    func.host_pattern = host_pattern
    return func
