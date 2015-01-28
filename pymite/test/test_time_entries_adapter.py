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

    #def by_id(self, id):
    #def from_to(self, fromdate, todate, limit=None, page=None):
    #def all(self, limit=None, page=None):
    #def create(self, date_at=None, minutes=0, note='', user_id=None,
    #           project_id=None, service_id=None):
    #def delete(self, id):


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

# vim: set ft=python ts=4 sw=4 expandtab :
