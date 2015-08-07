# -*- coding: utf-8 -*-
# File: test_daily_adapter.py
""" daily adapter test module. """

import urllib.request
from pymite.test.conftest import mock_urlopen, _get_url
from pymite.adapters import Daily


def test_daily_setup(libfactory):
    """ Test tracker setup. """
    factory = libfactory.daily_adapter
    assert factory is not None
    daily = Daily(factory.realm, factory.apikey)
    assert daily.adapter == 'daily'


def test_daily_at(monkeypatch, libfactory):
    daily = libfactory.daily_adapter
    at_data = [
        {'time_entry': {}},
        {'time_entry': {}}
    ]
    urlopen_at = mock_urlopen(at_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_at)

    at = daily.at('2015', '2', '2')
    assert at == list(map(lambda x: x['time_entry'], at_data))
    assert len(at) == len(at_data)


def test_daily_at_url(monkeypatch, libfactory):
    d = libfactory.daily_adapter

    monkeypatch.setattr(Daily, '_get', _get_url('time_entry'))
    url = d.at(2015, 2, 2)['api']
    assert url == 'https://foo.mite.yo.lk/daily/2015/2/2.json'
    url = d.at(2015, '2', '02')['api']
    assert url == 'https://foo.mite.yo.lk/daily/2015/2/2.json'


def test_daily_today(monkeypatch, libfactory):
    daily = libfactory.daily_adapter
    today_data = [
        {'time_entry': {}},
        {'time_entry': {}}
    ]
    urlopen_today = mock_urlopen(today_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_today)

    at = daily.today()
    assert at == list(map(lambda x: x['time_entry'], today_data))
    assert len(at) == len(today_data)


def test_daily_today_url(monkeypatch, libfactory):
    d = libfactory.daily_adapter

    monkeypatch.setattr(Daily, '_get', _get_url('time_entry'))
    url = d.today()['api']
    assert url == 'https://foo.mite.yo.lk/daily.json'

# vim: set ft=python ts=4 sw=4 expandtab :
