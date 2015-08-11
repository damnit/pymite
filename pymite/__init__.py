#  -*- coding: utf-8 -*-
#  File: __init__.py
""" adapter factory"""

__author__ = 'Otto Hockel'
__docformat__ = 'plaintext'


from pymite.adapters import (
    Tracker, Daily, Users, Projects, Customers, TimeEntries, Services
)


class Mite(object):
    """ API Factory that setups and returns the adapters
    """

    def __init__(self, realm, apikey):
        """ takes a valid realm and apikey. """
        self._apikey = apikey
        self._realm = realm

    @property
    def tracker_adapter(self):
        return Tracker(self._realm, self._apikey)

    @property
    def daily_adapter(self):
        return Daily(self._realm, self._apikey)

    @property
    def users_adapter(self):
        return Users(self._realm, self._apikey)

    @property
    def time_entries_adapter(self):
        return TimeEntries(self._realm, self._apikey)

    @property
    def customers_adapter(self):
        return Customers(self._realm, self._apikey)

    @property
    def services_adapter(self):
        return Services(self._realm, self._apikey)

    @property
    def projects_adapter(self):
        return Projects(self._realm, self._apikey)

# vim: set ft=python ts=4 sw=4 expandtab :
