# -*- coding: utf-8 -*-
# File: test_users_adapter.py
""" users adapter test module. """

import urllib.request
from .conftest import mock_urlopen, _get_url
from pymite.adapters import Users


def test_users_setup(libfactory):
    """ Test tracker setup. """
    factory = libfactory.users_adapter
    assert factory is not None
    us = Users(factory.realm, factory.apikey)
    assert us.adapter == 'users'


def test_users_all(monkeypatch, libfactory):
    us = libfactory.users_adapter
    us_data = [
        {'user': {}},
        {'user': {}}
    ]
    urlopen_us = mock_urlopen(us_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_us)

    active = us.all()
    assert active == list(map(lambda x: x['user'], us_data))
    assert len(active) == len(us_data)


def test_users_all_url(monkeypatch, libfactory):
    us = libfactory.users_adapter

    monkeypatch.setattr(Users, '_get', _get_url('user'))
    url = us.all()['api']
    assert url == 'https://foo.mite.yo.lk/users.json'
    url = us.all(archived=True)['api']
    assert url == 'https://foo.mite.yo.lk/users/archived.json'


def test_users_by_id(monkeypatch, libfactory):
    us = libfactory.users_adapter
    user_data = {'user': {}}
    urlopen_us = mock_urlopen(user_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_us)

    user = us.by_id(1)
    assert user == user_data['user']


def test_users_by_id_url(monkeypatch, libfactory):
    us = libfactory.users_adapter

    monkeypatch.setattr(Users, '_get', _get_url('user'))
    url = us.by_id(1)['api']
    assert url == 'https://foo.mite.yo.lk/users/1.json'

def test_users_by_mail(monkeypatch, libfactory):
    us = libfactory.users_adapter
    user_data = {'user': {
        'name': 'John Cleese', 'email': 'jc42@flying.circus'}
    }
    urlopen_us = mock_urlopen(user_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_us)

    user = us.by_mail('jc42@flying.circus')
    assert user == user_data['user']

    user_data = [
        {'user': {'name': 'John Cleese', 'email': 'jc42@flying.circus'}},
        {'user': {'name': 'Eric Idle', 'email': 'ei@flying.circus'}},
    ]
    urlopen_us = mock_urlopen(user_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_us)

    users = us.by_mail('@flying.circus')
    assert users == [user_data[0]['user'], user_data[1]['user']]


def test_users_by_mail_url(monkeypatch, libfactory):
    us = libfactory.users_adapter

    monkeypatch.setattr(Users, '_get', _get_url('user'))
    url = us.by_mail('jc42@flying.circus')['api']
    assert url == 'https://foo.mite.yo.lk/users.json?email=jc42%40flying.circus'

    monkeypatch.setattr(Users, '_get', _get_url('user'))
    url = us.by_mail('jc42@flying.circus', archived=True)['api']
    assert url == 'https://foo.mite.yo.lk/users/archived.json?email=jc42%40flying.circus'

# vim: set ft=python ts=4 sw=4 expandtab :
