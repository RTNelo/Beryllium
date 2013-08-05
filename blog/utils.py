#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides some simple and common function and class."""

import hashlib


def hash_repeat(raw, time=3):
    """This function will multi-hash a string and return the hash value.
    args:
        raw(str): the string you want to get hash value.
        time(int): how many times hash process would you like.
    return(str):
        The hash value of raw.
    """
    res = raw
    for i in xrange(time):
        res = hashlib.sha256(res).hexdigest()
    return res
