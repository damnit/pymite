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


# vim: set ft=python ts=4 sw=4 expandtab :
