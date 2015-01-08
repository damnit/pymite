# -*- coding: utf-8 -*-
#
# File: test_tracker_adapter.py
#
""" tracker adapter test module. """

__author__ = 'Otto Hockel <hockel.otto@gmail.com>'
__docformat__ = 'plaintext'

import pytest
import urllib.request
from pymite.test.conftest import mock_urlopen
from pymite.api.adapters import Tracker


def test_tracker_setup(libfactory):
    """ Test tracker setup. """
    factory_tracker = libfactory.tracker_adapter
    assert factory_tracker is not None
    tracker = Tracker(factory_tracker.realm, factory_tracker.apikey)
    assert tracker.adapter == 'tracker'


def test_tracker_show(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    # no tracker running
    tracker_data = {'tracker': {}}
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    show = tracker.show()
    assert show == tracker_data['tracker']

    # a tracker running
    tracker_data = {
        'tracker': {
            'tracking_time_entry': {
                'id': 31337, 'minutes': 42,
                'since': '2015-01-02T13:37:37+01:00'}
            }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    show = tracker.show()
    assert show == tracker_data['tracker']
    assert show['tracking_time_entry']['minutes'] == 42
    assert show['tracking_time_entry']['id'] == 31337


def test_tracker_start(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    # let's start a timer on an existing time entry
    tracker_data = {
        'tracker': {
            'tracking_time_entry': {
                'since': '2015-01-05T09:42:32+01:00',
                'minutes': 42, 'id': 42
            }
        }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    start = tracker.start(42)
    assert start == tracker_data['tracker']


def test_tracker_stop(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    tracker_data = {'tracker': {}}
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    with pytest.raises(Exception) as excinfo:
        tracker.stop(31337)
        assert excinfo.message == 'timer not running'

    # a timer running
    tracker_data = {
        'tracker': {
            'stopped_time_entry': {
                'id': 24, 'minutes': 42}
        }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    # this test passes as we provide an id
    stop = tracker.stop(24)
    assert stop == tracker_data['tracker']
    assert stop['stopped_time_entry']['minutes'] == 42
    assert stop['stopped_time_entry']['id'] == 24

# vim: set ft=python ts=4 sw=4 expandtab :
