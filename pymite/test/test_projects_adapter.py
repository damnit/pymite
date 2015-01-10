# -*- coding: utf-8 -*-
#
# File: test_projects_adapter.py
#
""" projects adapter test module. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import pytest
import urllib.request
from pymite.test.conftest import mock_urlopen
from pymite.api.adapters import Projects


def test_projects_setup(libfactory):
    """ Test tracker setup. """
    factory_projects = libfactory.projects_adapter
    assert factory_projects is not None
    projects = Projects(factory_projects.realm, factory_projects.apikey)
    assert projects.adapter == 'projects'


def test_projects_all(monkeypatch, libfactory):
    projects = Projects(libfactory.projects_adapter.realm,
                        libfactory.projects_adapter.apikey)

    # query all projects
    all_data = [
        {'project': {'id': 1, 'archived': False, 'customer_name': 'John Cleese',
                     'name': 'Bicycle Repair Man', 'note':
                     'https://www.youtube.com/watch?v=rxfzm9dfqBw'}},
        {'project': {'id': 2, 'archived': False, 'customer_name': 'Erid Idle',
                     'name': 'Biggus Dickus', 'note':
                     'https://www.youtube.com/watch?v=2K8_jgiNqUc'}}
    ]
    urlopen_projects = mock_urlopen(all_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_projects)

    all_projects = projects.all()
    assert all_projects == list(map(lambda x: x['project'], all_data))

# vim: set ft=python ts=4 sw=4 expandtab :

