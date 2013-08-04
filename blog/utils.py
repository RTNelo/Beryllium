#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides some simple and common function and class.
"""

import hashlib


def hash_repeat(raw, time=3):
    """
    This function will multi-hash a string and return the hash value.
    Raw is a string that you want to get hash value.
    Time is a int value represent how many times hash would you like.
    """
    res = raw
    for i in xrange(time):
        res = hashlib.sha256(res).hexdigest()
    return res
