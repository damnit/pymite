# -*- coding: utf-8 -*-
#
# File: conftest.py
#
""" Conftest file that sets up the unit tests."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import json
import pytest
from io import BytesIO
from pymite.api import Mite
from pymite.api.mite import MiteAPI


def mock_urlopen(json_data, resp_code=200):
    """ closure to parametrize the urlopen mockage. """
    def mockreturn(*args, **kwargs):
        buf = BytesIO()
        bytedump = bytes(json.dumps(json_data), encoding='UTF-8')
        buf.write(bytedump)
        buf.seek(0)
        buf.code = resp_code
        return buf
    return mockreturn


@pytest.fixture(scope='session')
def libfactory():
    """ setup the api factory using dummy data. """
    return Mite('foo', 'bar')


@pytest.fixture(scope='session')
def base_api():
    """ setup the base api class using dummy data. """
    return MiteAPI('foo', 'bar')

# vim: set ft=python ts=4 sw=4 expandtab :
