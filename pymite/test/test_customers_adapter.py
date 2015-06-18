# -*- coding: utf-8 -*-
# File: test_customers_adapter.py
""" customers adapter test module. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import urllib.request
from pymite.test.conftest import mock_urlopen, _get_url, parse_params
from pymite.api.adapters import Customers


def test_customers_setup(libfactory):
    """ Test tracker setup. """
    factory = libfactory.customers_adapter
    assert factory is not None
    customers = Customers(factory.realm, factory.apikey)
    assert customers.adapter == 'customers'


def test_customers_all(monkeypatch, libfactory):
    customers = libfactory.customers_adapter
    all_data = [
        {'customer': {'active_hourly_rate': 900,
                      'hourly_rates_per_service': [], 'hourly_rate': 900,
                      'id': 24, 'name': 'John Cleese',
                      'created_at': '2000-01-01T08:15:42+02:00', 'note': '',
                      'archived': False,
                      'updated_at': '2000-01-02T04:71:11+02:00'}},
        {'customer': {'active_hourly_rate': 900,
                      'hourly_rates_per_service': [], 'hourly_rate': 900,
                      'id': 42, 'name': 'Eric Idle',
                      'created_at': '2000-01-02T08:15:42+02:00', 'note': '',
                      'archived': False,
                      'updated_at': '2000-01-03T04:71:11+02:00'}}
    ]
    urlopen_customers = mock_urlopen(all_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_customers)

    all_customers = customers.all()
    assert all_customers == list(map(lambda x: x['customer'], all_data))
    assert len(all_customers) == len(all_data)


def test_customers_all_url(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.all()['api']
    assert url == 'https://foo.mite.yo.lk/customers.json'

    url = customers.all(archived=True)['api']
    assert url == 'https://foo.mite.yo.lk/customers/archived.json'


def test_customers_all_limited(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.all(limit=20)['api']
    assert url == 'https://foo.mite.yo.lk/customers.json?limit=20'


def test_customers_all_paginated(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.all(page=5)['api']
    assert url == 'https://foo.mite.yo.lk/customers.json?page=5'


def test_customers_all_paginated_limited(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.all(limit=4, page=5)['api']
    assert ('https://foo.mite.yo.lk/customers.json?' in url)
    assert {'limit': '4', 'page': '5'} == parse_params(url)


def test_customers_by_id(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    customer_data = {'customer': {'active_hourly_rate': 900,
                                  'hourly_rates_per_service': [],
                                  'hourly_rate': 900,
                                  'id': 24, 'name': 'John Cleese',
                                  'created_at': '2000-01-01T08:15:42+02:00',
                                  'note': '', 'archived': False,
                                  'updated_at': '2000-01-02T04:71:11+02:00'}}
    urlopen_customer = mock_urlopen(customer_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_customer)

    cleese = customers.by_id(24)

    assert cleese == customer_data['customer']
    assert cleese['id'] == 24
    assert cleese['name'] == 'John Cleese'


def test_customers_by_id_url(monkeypatch, libfactory):
    customers = libfactory.customers_adapter

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.by_id(42)['api']
    assert url == 'https://foo.mite.yo.lk/customers/42.json'


def test_customers_by_name(monkeypatch, libfactory):
    customers = libfactory.customers_adapter


    customer_data = {'customer': {'active_hourly_rate': 900,
                                  'hourly_rates_per_service': [],
                                  'hourly_rate': 900,
                                  'id': 24, 'name': 'John Cleese',
                                  'created_at': '2000-01-01T08:15:42+02:00',
                                  'note': '', 'archived': False,
                                  'updated_at': '2000-01-02T04:71:11+02:00'}}
    urlopen_customer = mock_urlopen(customer_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_customer)

    cleese = customers.by_name('John Cleese')

    assert cleese == customer_data['customer']
    assert cleese['id'] == 24
    assert cleese['name'] == 'John Cleese'

    # test an archived customer
    customer_data['customer']['archived'] = True
    urlopen_customer = mock_urlopen(customer_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_customer)

    cleese = customers.by_name('John Cleese', archived=True)
    assert cleese['archived'] is True


def test_customers_by_name_url(monkeypatch, libfactory):
    customers = libfactory.customers_adapter
    base_url = 'https://foo.mite.yo.lk/customers'

    monkeypatch.setattr(Customers, '_get', _get_url('customer'))
    url = customers.by_name('Eric Idle', archived=True)['api']
    assert url == '%s/archived.json?name=Eric+Idle' % base_url

    url = customers.by_name('Eric Idle')['api']
    assert url == '%s.json?name=Eric+Idle' % base_url

    url = customers.by_name('Eric Idle', archived=True)['api']
    assert url == '%s/archived.json?name=Eric+Idle' % base_url


# vim: set ft=python ts=4 sw=4 expandtab :
