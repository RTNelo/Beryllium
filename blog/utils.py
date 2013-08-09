#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides some simple and common function and class."""

import hashlib
import datetime
import functools

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
