# -*- coding: utf-8 -*-
# File: test_time_entries_adapter.py
""" time entries adapter test module. """

import urllib.request
from pymite.test.conftest import mock_urlopen, _get_url
from pymite.api.adapters import TimeEntries


def test_time_entries_setup(libfactory):
    """ Test tracker setup. """
    factory = libfactory.time_entries_adapter
    assert factory is not None
    te = TimeEntries(factory.realm, factory.apikey)
    assert te.adapter == 'time_entries'


def test_time_entries_at(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    at_data = [
        {'time_entry': {}},
        {'time_entry': {}}
    ]
    urlopen_at = mock_urlopen(at_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_at)
    at = te.at('2015-02-02')
    assert at == list(map(lambda x: x['time_entry'], at_data))
    assert len(at) == len(at_data)


def test_time_entries_at_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.at('2015-02-02')['api']
    assert url == 'https://foo.mite.yo.lk/time_entries.json?at=2015-02-02'


def test_time_entries_by_id(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    te_data = {'time_entry': {}}
    urlopen_te = mock_urlopen(te_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_te)
    time = te.by_id(42)
    assert time == te_data['time_entry']


def test_time_entries_by_id_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.by_id(42)['api']
    assert url == 'https://foo.mite.yo.lk/time_entries/42.json'


def test_time_entries_all(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    all_data = [{'time_entry': {}} for _ in range(100)]
    urlopen_all = mock_urlopen(all_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_all)
    time_entries = te.all()
    assert time_entries == list(map(lambda x: x['time_entry'], all_data))
    assert len(time_entries) == len(all_data)


def test_time_entries_all_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.all()['api']
    assert url == 'https://foo.mite.yo.lk/time_entries.json'


def test_time_entries_all_paginated_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.all(limit=10)['api']
    assert url == 'https://foo.mite.yo.lk/time_entries.json?limit=10'


def test_time_entries_from_to(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    ft_data = [{'time_entry': {}} for _ in range(1000)]
    urlopen_ft = mock_urlopen(ft_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_ft)
    ft = te.from_to('2015-02-02', '2015-02-14')
    assert ft == list(map(lambda x: x['time_entry'], ft_data))
    assert len(ft) == len(ft_data)


def test_time_entries_from_to_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.from_to('2015-02-02', '2015-02-14')['api']
    base_url = 'https://foo.mite.yo.lk/time_entries.json'
    get_data = '?from=2015-02-02&to=2015-02-14'
    assert url == '%s%s' % (base_url, get_data)


def test_time_entries_from_to_paginated_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.from_to('2015-02-02', '2015-02-14', page=4)['api']
    base_url = 'https://foo.mite.yo.lk/time_entries.json'
    get_data = '?from=2015-02-02&page=4&to=2015-02-14'
    assert url == '%s%s' % (base_url, get_data)


# TODO:
#    def create(self, date_at=None, minutes=0, note='', user_id=None,
#               project_id=None, service_id=None)
#    delete(self, id)

# vim: set ft=python ts=4 sw=4 expandtab :
