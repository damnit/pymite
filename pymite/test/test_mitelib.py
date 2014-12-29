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


def test_setup(monkeypatch, libfactory):
    assert monkeypatch is not None
    assert libfactory is not None

    def mockmyselfreturn(*args, **kwargs):
        buf = BytesIO()
        bytedump = bytes(json.dumps(MYSELF), encoding='UTF-8')
        buf.write(bytedump)
        buf.seek(0)
        return buf

    monkeypatch.setattr(urllib.request, 'urlopen', mockmyselfreturn)
    daily = libfactory.daily_adapter
    assert daily.myself == MYSELF['user']

# vim: set ft=python ts=4 sw=4 expandtab :
