# -*- coding: utf-8 -*-
# File: test_time_entries_adapter.py
""" time entries adapter test module. """

import urllib.request
import json
from .conftest import (
        mock_urlopen, _get_url, _post_url, _delete_url, parse_params
)
from pymite.adapters import TimeEntries


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
    at = te.query(at='2015-02-02')
    assert at == list(map(lambda x: x['time_entry'], at_data))
    assert len(at) == len(at_data)


def test_time_entries_at_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.query(at='2015-02-02')['api']
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
    time_entries = te.query()
    assert time_entries == list(map(lambda x: x['time_entry'], all_data))
    assert len(time_entries) == len(all_data)


def test_time_entries_all_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.query()['api']
    assert url == 'https://foo.mite.yo.lk/time_entries.json'


def test_time_entries_all_limited_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    url = te.query(limit=10)['api']
    assert url == 'https://foo.mite.yo.lk/time_entries.json?limit=10'


def test_time_entries_from_to(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    ft_data = [{'time_entry': {}} for _ in range(1000)]
    urlopen_ft = mock_urlopen(ft_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_ft)
    kws = {'from': '2015-02-02', 'to': '2015-02-14'}
    ft = te.query(**kws)
    assert ft == list(map(lambda x: x['time_entry'], ft_data))
    assert len(ft) == len(ft_data)


def test_time_entries_from_to_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    kws = {'from': '2015-02-02', 'to': '2015-02-14'}
    url = te.query(**kws)['api']


def test_time_entries_from_to_paginated_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_get', _get_url('time_entry'))
    kws = {'from': '2015-02-02', 'to': '2015-02-14', 'page': '4'}
    url = te.query(**kws)['api']
    assert ('https://foo.mite.yo.lk/time_entries.json?' in url)
    assert kws == parse_params(url)


def test_time_entries_delete(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    # ft_data = {'success': 200}
    ft_data = b' '
    urlopen_ft = mock_urlopen(ft_data, resp_code=200)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_ft)
    ft = te.delete(42)
    assert ft == {'success': 200}


def test_time_entries_delete_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_delete', _delete_url(200))
    data = te.delete(1337)
    base_url = 'https://foo.mite.yo.lk/time_entries/1337.json'
    assert data['api'] == base_url
    assert data['code'] == 200
    assert data['method'] == 'DELETE'


def test_time_entries_create(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter
    cr_data = {'time_entry': {}}
    urlopen_cr = mock_urlopen(cr_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_cr)
    cr = te.create(minutes=42, note='foo', user_id=666)
    assert cr == cr_data['time_entry']


def test_time_entries_create_url(monkeypatch, libfactory):
    te = libfactory.time_entries_adapter

    monkeypatch.setattr(TimeEntries, '_post', _post_url(201))
    post_data = {'time_entry': {'minutes': 42, 'user_id': 123, 'note': 'bam'}}
    data = te.create(**post_data['time_entry'])
    base_url = 'https://foo.mite.yo.lk/time_entries.json'
    assert data['api'] == base_url
    assert data['code'] == 201
    assert data['method'] == 'POST'
    assert json.loads(data['data'].decode()) == post_data

# vim: set ft=python ts=4 sw=4 expandtab :
