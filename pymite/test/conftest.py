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


def _get_url(adapter_class):
    """ closure to parametrize the adapter class. """
    def _get(self, path, **kwargs):
        """ a short version of MiteAPI._get to check the built url.
        """
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        data = urllib.parse.urlencode(kwargs)
        if len(data) > 0:
            api = self._api('%s.json?%s' % (path, data))
        else:
            api = self._api('%s.json' % path)
        return {adapter_class: {'api': api, 'data': data}}
    return _get


def _post_url(adapter_class):
    """ closure to parametrize the adapter class. """
    def _post(self, path, **kwargs):
        """ a short version of MiteAPI._post to check the built url.
        """
        kwargs = {k: v for k, v in kwargs.items() if v is not ('' or None)}
        data = bytes(json.dumps(kwargs), encoding='UTF-8')
        # change content type on post
        self._headers['Content-Type'] = 'application/json'
        api = self._api('%s.json' % path)
        return {adapter_class: {'api': api, 'data': data}}
    return _post


def _put_url(adapter_class):
    """ closure to parametrize the adapter class. """
    def _put(self, path, **kwargs):
        """ a short version of MiteAPI._put to check the built url.
        """
        kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}
        data = urllib.parse.urlencode(kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
        return {adapter_class: {'api': api, 'data': data}}
    return _put


def _delete_url(adapter_class):
    """ a short version of MiteAPI._delete to check the built url.
    """
    def _delete(self, path, **kwargs):
        """ return a dict. """
        kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}
        data = urllib.parse.urlencode(kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
        return {adapter_class: {'api': api, 'data': data}}
    return _delete


@pytest.fixture(scope='session')
def libfactory():
    """ setup the api factory using dummy data. """
    return Mite('foo', 'bar')


@pytest.fixture(scope='session')
def base_api():
    """ setup the base api class using dummy data. """
    return MiteAPI('foo', 'bar')

# vim: set ft=python ts=4 sw=4 expandtab :
