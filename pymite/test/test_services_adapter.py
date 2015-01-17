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
    factory_services = libfactory.projects_adapter
    assert factory_services is not None
    services = Services(factory_projects.realm, factory_projects.apikey)
    assert services.adapter == 'services'


# vim: set ft=python ts=4 sw=4 expandtab :
