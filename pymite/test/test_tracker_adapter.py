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
        assert excinfo.message == 'no timer running'

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

    # this test passes as we provide an id
    stop = tracker.stop(id=24)
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
        assert excinfo.message == 'no timer running'

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
        assert excinfo.message == 'no timer running'

    # the last property should remain unchanged
    assert tracker.last is not None
    assert tracker.last == 24


def test_tracker_start(monkeypatch, libfactory):
    tracker = Tracker(libfactory.tracker_adapter.realm,
                      libfactory.tracker_adapter.apikey)

    # a fresh setup
    assert tracker.last is None
    assert tracker.actual is None

    with pytest.raises(Exception) as excinfo:
        tracker.start()
        assert excinfo.message == 'no id provided and no last timer id saved.'

    # now let's start a timer on an existing time entry
    tracker_data = {
        'tracker': {
            'tracking_time_entry': {
                'since':'2015-01-05T09:42:32+01:00',
                'minutes': 42, 'id': 42
            }
        }
    }
    urlopen_tracker = mock_urlopen(tracker_data)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_tracker)

    start = tracker.start(id=42)
    assert start == tracker_data['tracker']
    assert tracker.actual is 42
    assert tracker.last is None

    # let's stop it and start it again
    tracker._last = 42
    tracker._actual = None
    tracker.start()

    assert start == tracker_data['tracker']
    assert tracker.actual is 42
    assert tracker.last is 42

# vim: set ft=python ts=4 sw=4 expandtab :
