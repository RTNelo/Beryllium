#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module provides some simple and common function and class."""

import hashlib


def hash_repeat(raw, salt_pre='', salt_suf='', time=3):
    """This function will multi-hash a string and return the hash value.
    args:
        raw(str): the string you want to get hash value.
        salt_pre(str): the salt added before the raw.
        salt_suf(str): the salt added after the raw.
        time(int): how many times hash process would you like.
    return(str):
        The hash value of raw.
    """
    res = raw
    for i in xrange(time):
        res = hashlib.sha256(''.join((salt_pre, res, salt_suf))).hexdigest()
    return res
