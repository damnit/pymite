# -*- coding: utf-8 -*-
#
# File: conftest.py
#
""" Conftest file that sets up the unit tests."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import pytest
from pymite.api import Mite
from pymite.api.mite import MiteAPI


@pytest.fixture(scope='session')
def libfactory():
    """ setup the api factory using dummy data. """
    return Mite('foo', 'bar')


@pytest.fixture(scope='session')
def base_api():
    """ setup the base api class using dummy data. """
    return MiteAPI('foo', 'bar')

# vim: set ft=python ts=4 sw=4 expandtab :
