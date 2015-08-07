# -*- coding: utf-8 -*-
#
# File: test_utils.py
#
""" utils test module."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

from pymite.utils import declassify


def test_declassify_single():
    """ Test declassify decorator. """
    @declassify('foo')
    def foo():
        return {'foo': {}}
    assert foo() == {}


def test_declassify_multi():
    """ Test declassify decorator. """
    @declassify('foo')
    def foo():
        return [{'foo': {}} for _ in range(1000)]
    assert foo() == [{} for _ in range(1000)]


def test_declassify_error():
    """ Test declassify decorator.
    In case of an error, just return the data.
    """
    @declassify('bar')
    def foo():
        return {'foo': {}}
    assert foo() == {'foo': {}}

# vim: set ft=python ts=4 sw=4 expandtab :
