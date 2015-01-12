# -*- coding: utf-8 -*-
#
# File: conftest.py
#
""" Conftest file that sets up the unit tests."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import json
import pytest
import urllib
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


def url__get(self, path, **kwargs):
    """ a short version of MiteAPI._get to check the built url.
    """
    kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}
    data = urllib.parse.urlencode(kwargs)
    if data:
        api = self._api('%s.json?%s' % (path, data))
    else:
        api = self._api('%s.json' % path)
    return {'project': api}


@pytest.fixture(scope='session')
def libfactory():
    """ setup the api factory using dummy data. """
    return Mite('foo', 'bar')


@pytest.fixture(scope='session')
def base_api():
    """ setup the base api class using dummy data. """
    return MiteAPI('foo', 'bar')

# vim: set ft=python ts=4 sw=4 expandtab :
