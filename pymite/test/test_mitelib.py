# -*- coding: utf-8 -*-
# File: test_mitelib.py
""" test module to test the mite library wrapper. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import urllib.request
from pymite.test.conftest import mock_urlopen


def test_setup(libfactory):
    assert libfactory is not None


def test_factory_properties(libfactory):
    assert libfactory._apikey == 'bar'
    assert libfactory._realm == 'foo'
    adapters = ['tracker', 'daily', 'users', 'time_entries', 'customers',
                'services', 'projects']
    for adapter in adapters:
        assert libfactory.__getattribute__('%s_adapter' % adapter)


def test_base_api_properties(monkeypatch, base_api):
    """we do not process data except the declassification of some
    top level properties.
    """

    assert base_api.realm == 'foo'
    assert base_api._realm == 'foo'

    assert base_api.apikey == 'bar'
    assert base_api._apikey == 'bar'

    headers = {
        'X-MiteApiKey': 'bar',
        'Content-Type': 'text/json',
        'User-Agent': 'pymite/dev (https://github.com/damnit)'
    }

    assert base_api._headers == headers

    assert base_api._api('baz') == 'https://foo.mite.yo.lk/baz'


def test_base_api_myself(monkeypatch, base_api):
    """ Test myself adapter property. """
    myself = {'user': {}}

    urlopen_myself = mock_urlopen(myself)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_myself)

    assert base_api.myself == myself['user']


def test_base_api_account(monkeypatch, base_api):
    """ Test account adapter property. """
    account = {'account': {}}

    urlopen_account = mock_urlopen(account)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_account)

    assert base_api.account == account['account']

# vim: set ft=python ts=4 sw=4 expandtab :
