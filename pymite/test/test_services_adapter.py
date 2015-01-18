# -*- coding: utf-8 -*-
# File: test_services_adapter.py
""" services adapter test module. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import urllib.request
from pymite.test.conftest import mock_urlopen, _get_url
from pymite.api.adapters import Services


def test_services_setup(libfactory):
    """ Test tracker setup. """
    factory = libfactory.services_adapter
    assert factory is not None
    services = Services(factory.realm, factory.apikey)
    assert services.adapter == 'services'


def test_services_all(monkeypatch, libfactory):
    services = libfactory.services_adapter
    all_data = [
        {'service': {'id': 1, 'archived': False, 'billable': True,
                     'note': 'foo', 'name': 'consulting', 'hourly_rate': 3300,
                     'created_at': '2014-12-12T13:37:37+01:00',
                     'updated_at': '2014-12-13T13:37:37+01:00',}},
        {'service': {'id': 2, 'archived': False, 'billable': True,
                     'note': 'bar', 'name': 'testing', 'hourly_rate': 4200,
                     'created_at': '2014-12-12T13:37:37+01:00',
                     'updated_at': '2014-12-13T13:37:37+01:00',}},
    ]
    urlopen_services = mock_urlopen(all_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_services)

    all_services = services.all()
    assert all_services == list(map(lambda x: x['service'], all_data))
    assert len(all_services) == len(all_data)


def test_services_all_url(monkeypatch, libfactory):
    services = libfactory.services_adapter

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.all()['api']
    assert url == 'https://foo.mite.yo.lk/services.json'

    url = services.all(archived=True)['api']
    assert url == 'https://foo.mite.yo.lk/services/archived.json'


def test_services_all_limited(monkeypatch, libfactory):
    services = libfactory.services_adapter

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.all(limit=20)['api']
    assert url == 'https://foo.mite.yo.lk/services.json?limit=20'


def test_services_all_paginated(monkeypatch, libfactory):
    services = libfactory.services_adapter

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.all(page=5)['api']
    assert url == 'https://foo.mite.yo.lk/services.json?page=5'


def test_services_all_paginated_limited(monkeypatch, libfactory):
    services = libfactory.services_adapter

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.all(limit=4, page=5)['api']
    assert url == 'https://foo.mite.yo.lk/services.json?limit=4&page=5'


def test_services_by_id(monkeypatch, libfactory):
    services = libfactory.services_adapter

    service_data = {'service': {'id': 42, 'archived': False,
                                'billable': True, 'note': 'foo',
                                'name': 'consulting', 'hourly_rate': 3300,
                                'created_at': '2014-12-12T13:37:37+01:00',
                                'updated_at': '2014-12-13T13:37:37+01:00',}}
    urlopen_service = mock_urlopen(service_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_service)

    consulting = services.by_id(42)

    assert consulting == service_data['service']
    assert consulting['id'] == 42
    assert consulting['name'] == 'consulting'


def test_services_by_id_url(monkeypatch, libfactory):
    services = libfactory.services_adapter

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.by_id(42)['api']
    assert url == 'https://foo.mite.yo.lk/services/42.json'


def test_services_by_name(monkeypatch, libfactory):
    services = libfactory.services_adapter

    service_data = {'service': {'id': 42, 'archived': False,
                                'billable': True, 'note': 'foo',
                                'name': 'consulting', 'hourly_rate': 3300,
                                'created_at': '2014-12-12T13:37:37+01:00',
                                'updated_at': '2014-12-13T13:37:37+01:00',}}
    urlopen_service = mock_urlopen(service_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_service)

    consulting = services.by_name('consulting')

    assert consulting == service_data['service']
    assert consulting['id'] == 42
    assert consulting['name'] == 'consulting'

    # test an archived service
    service_data['service']['archived'] = True
    urlopen_service = mock_urlopen(service_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_service)

    consulting = services.by_name('consulting', archived=True)
    assert consulting['archived'] is True


def test_services_by_name_url(monkeypatch, libfactory):
    services = libfactory.services_adapter
    base_url = 'https://foo.mite.yo.lk/services'

    monkeypatch.setattr(Services, '_get', _get_url('service'))
    url = services.by_name('consulting', archived=True)['api']
    assert url == '%s/archived.json?name=consulting' % base_url

    url = services.by_name('consulting')['api']
    assert url == '%s.json?name=consulting' % base_url

    url = services.by_name('consulting', archived=True)['api']
    assert url == '%s/archived.json?name=consulting' % base_url


# vim: set ft=python ts=4 sw=4 expandtab :
