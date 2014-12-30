# -*- coding: utf-8 -*-
#
# File: test_mitelib.py
#
""" pep257 compliant module documentation."""

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import urllib.request
from io import BytesIO
import json

MYSELF = {
    'user': {
        'role': 'time_tracker',
        'updated_at': '2014-12-18T13:37:00+01:00',
        'email': 'foo@manc.hu',
        'name': 'Foo Manchu',
        'note': '',
        'created_at': '2013-06-18T13:37:13+02:00',
        'language': 'de',
        'archived': False,
        'id': 1
    }
}

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


def test_properties(libfactory):
    assert libfactory._apikey == 'bar'
    assert libfactory._realm == 'foo'
    adapters = ['tracker', 'daily', 'users', 'time_entries', 'customers',
                'services', 'projects']
    for adapter in adapters:
        assert libfactory.__getattribute__('%s_adapter' % adapter)


def test_base_api(monkeypatch, base_api):
    urlopen_myself = mock_urlopen(MYSELF)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_myself)
    assert base_api.myself == MYSELF['user']
    assert base_api.realm == 'foo'
    assert base_api.apikey == 'bar'
    assert base_api._api('baz') == 'https://foo.mite.yo.lk/baz'

# vim: set ft=python ts=4 sw=4 expandtab :
