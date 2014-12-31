# -*- coding: utf-8 -*-
#
# File: test_mitelib.py
#
""" test module to test the mite library wrapper. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import urllib.request
from io import BytesIO
import json


def mock_urlopen(json_data):
    """ closure to parametrize the urlopen mockage. """
    def mockreturn(*args, **kwargs):
        buf = BytesIO()
        bytedump = bytes(json.dumps(json_data), encoding='UTF-8')
        buf.write(bytedump)
        buf.seek(0)
        return buf
    return mockreturn


def test_setup(libfactory):
    assert libfactory is not None


def test_factory_properties(libfactory):
    assert libfactory._apikey == 'bar'
    assert libfactory._realm == 'foo'
    adapters = ['tracker', 'daily', 'users', 'time_entries', 'customers',
                'services', 'projects']
    for adapter in adapters:
        assert libfactory.__getattribute__('%s_adapter' % adapter)


def test_base_api(monkeypatch, base_api):
    """we do not process data except the declassification of some
    top level properties.
    """

    assert base_api.realm == 'foo'
    assert base_api.apikey == 'bar'
    assert base_api._api('baz') == 'https://foo.mite.yo.lk/baz'

    myself = {'user': {}}

    urlopen_myself = mock_urlopen(myself)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_myself)

    assert base_api.myself == myself['user']

    account = {'account': {}}

    urlopen_account = mock_urlopen(account)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_account)

    assert base_api.account == account['account']

# vim: set ft=python ts=4 sw=4 expandtab :
