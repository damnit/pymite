# -*- coding: utf-8 -*-
# File: test_data.py
""" we should store json files and read them through this module. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

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

ACCOUNT = {
    'account': {
        'currency': 'EUR',
        'updated_at': '2014-12-07T13:37:13+02:00',
        'created_at': '2013-01-01T13:37:13+02:00',
        'name': 'foocorp',
        'id': 123,
        'title': 'foocorp'}
}

# vim: set ft=python ts=4 sw=4 expandtab :
