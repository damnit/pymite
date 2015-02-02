# -*- coding: utf-8 -*-
# File: conftest.py
""" Conftest file that sets up the unit tests."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import json
import pytest
import urllib
from collections import OrderedDict
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
        # clean kwargs (filter None and empty string)
        clean_kwargs = filter(lambda x: 1 if x[1] else 0, kwargs.items())
        clean_kwargs = OrderedDict(sorted(list(clean_kwargs)))

        data = urllib.parse.urlencode(clean_kwargs)
        if len(data) > 0:
            api = self._api('%s.json?%s' % (path, data))
        else:
            api = self._api('%s.json' % path)
        return {adapter_class: {'api': api, 'data': data}}
    return _get


def _post_url(resp_code):
    """ closure to parametrize the adapter class. """
    def _post(self, path, **kwargs):
        """ a short version of MiteAPI._post to check the built url.
        """
        # clean kwargs (filter None and empty string)
        clean_kwargs = filter(lambda x: 1 if x[1] else 0, kwargs.items())
        clean_kwargs = OrderedDict(sorted(list(clean_kwargs)))

        data = bytes(json.dumps(clean_kwargs), encoding='UTF-8')
        # change content type on post
        self._headers['Content-Type'] = 'application/json'
        api = self._api('%s.json' % path)
        return {'api': api, 'data': data, 'code': resp_code, 'method': 'POST'}
    return _post


def _put_url(resp_code):
    """ closure to parametrize the adapter class. """
    def _put(self, path, **kwargs):
        """ a short version of MiteAPI._put to check the built url.
        """
        # clean kwargs (filter None and empty string)
        clean_kwargs = filter(lambda x: 1 if x[1] else 0, kwargs.items())
        clean_kwargs = OrderedDict(sorted(list(clean_kwargs)))

        data = urllib.parse.urlencode(clean_kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
        return {'api': api, 'data': data, 'code': resp_code, 'method': 'PUT'}
    return _put


def _delete_url(resp_code):
    """ a short version of MiteAPI._delete to check the built url.
    """
    def _delete(self, path, **kwargs):
        """ return a dict. """
        # clean kwargs (filter None and empty string)
        clean_kwargs = filter(lambda x: 1 if x[1] else 0, kwargs.items())
        clean_kwargs = OrderedDict(sorted(list(clean_kwargs)))

        data = urllib.parse.urlencode(clean_kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
        return {'api': api, 'data': data, 'code': resp_code, 'method': 'DELETE'}
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
