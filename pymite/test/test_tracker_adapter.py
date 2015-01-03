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

    # the properties should be `None` after initialization
    assert tracker.actual is None
    assert tracker.last is None
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
    assert tracker.actual is None

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
    assert tracker.actual is not None
    assert tracker.actual == 31337


def test_tracker_stop_no_state_check(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    # state not checked and no timer running
    assert tracker.actual is None

    tracker_data = {'tracker': {}}
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    with pytest.raises(Exception) as excinfo:
        tracker.stop()
        assert excinfo.message == 'No timer running'

    assert tracker.actual is None
    assert tracker.last is None

    # state not checked and a timer running
    tracker_data = {
        'tracker': {
            'stopped_time_entry': {
                'id': 24, 'minutes': 42}
        }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    stop = tracker.stop()
    assert stop == tracker_data['tracker']
    assert stop['stopped_time_entry']['minutes'] == 42
    assert stop['stopped_time_entry']['id'] == 24
    assert tracker.last is not None
    assert tracker.last == 24


def test_tracker_stop_state_check(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    # state checked (no actual and no last), no timer running
    assert tracker.actual is None

    tracker_data = {'tracker': {}}
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    with pytest.raises(Exception) as excinfo:
        tracker.stop()
        assert excinfo.message == 'No timer running'

    assert tracker.actual is None
    assert tracker.last is None

    # state checked (actual running timer) and a timer running
    tracker._actual = 24

    tracker_data = {
        'tracker': {
            'stopped_time_entry': {
                'id': 24, 'minutes': 42}
        }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    stop = tracker.stop()
    assert stop == tracker_data['tracker']
    assert tracker.last is not None
    assert tracker.last == 24

    # state checked (last timer saved), no timer running
    with pytest.raises(Exception) as excinfo:
        tracker.stop()
        assert excinfo.message == 'No timer running'

    # the last property should remain unchanged
    assert tracker.last is not None
    assert tracker.last == 24

# vim: set ft=python ts=4 sw=4 expandtab :
