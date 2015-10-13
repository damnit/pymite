# -*- coding: utf-8 -*-
# File: adapters.py
""" api adapters module. """

from functools import partial
from pymite.mite import MiteAPI
from pymite.utils import declassify


def _path(*args):
    return '/'.join([str(arg) for arg in args])


class DefaultReadAdapter(MiteAPI):

    def __init__(self, realm, apikey):
        super(MiteAPI, self).__init__(realm, apikey)

    def by_id(self, id):
        """get adapter data by its id."""
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path)

    def by_name(self, name, archived=False, limit=None, page=None):
        """get adapter data by name."""
        if not archived:
            path = _path(self.adapter)
        else:
            path = _path(self.adapter, 'archived')
        return self._get(path, name=name, limit=limit, page=page)

    def all(self, archived=False, limit=None, page=None):
        """get all adapter data."""
        path = partial(_path, self.adapter)
        if not archived:
            path = _path(self.adapter)
        else:
            path = _path(self.adapter, 'archived')
        return self._get(path, limit=limit, page=page)


class Projects(DefaultReadAdapter):
    """ the projects class. """

    def __init__(self, realm, apikey):
        super(DefaultReadAdapter, self).__init__(realm, apikey)
        self._adapter = 'projects'

    @declassify('project')
    def by_id(self, id):
        """ return a project by it's id. """
        return super(Projects, self).by_id(id)

    @declassify('project')
    def by_name(self, name, archived=False, limit=None, page=None):
        """ return a project by it's name.
        this only works with the exact name of the project.
        """
        # this only works with the exact name
        return super(Projects, self).by_name(name, archived=archived,
                                             limit=limit, page=page)

    @declassify('project')
    def all(self, archived=False, limit=None, page=None):
        return super(Projects, self).all(archived=archived,
                                         limit=limit, page=page)


class Services(DefaultReadAdapter):
    """ the services class. """

    def __init__(self, realm, apikey):
        super(DefaultReadAdapter, self).__init__(realm, apikey)
        self._adapter = 'services'

    @declassify('service')
    def by_id(self, id):
        return super(Services, self).by_id(id)

    @declassify('service')
    def by_name(self, name, archived=False, limit=None, page=None):
        return super(Services, self).by_name(name, archived=archived,
                                             limit=limit, page=page)

    @declassify('service')
    def all(self, archived=False, limit=None, page=None):
        return super(Services, self).all(archived=archived,
                                         limit=limit, page=page)


class Customers(DefaultReadAdapter):
    """ the customers class. """

    def __init__(self, realm, apikey):
        super(DefaultReadAdapter, self).__init__(realm, apikey)
        self._adapter = 'customers'

    @declassify('customer')
    def by_id(self, id):
        return super(Customers, self).by_id(id)

    @declassify('customer')
    def by_name(self, name, archived=False, limit=None, page=None):
        return super(Customers, self).by_name(name, archived=archived,
                                              limit=limit, page=page)

    @declassify('customer')
    def all(self, archived=False, limit=None, page=None):
        return super(Customers, self).all(archived=archived,
                                          limit=limit, page=page)


class Users(MiteAPI):
    """ the users class. """

    def __init__(self, realm, apikey):
        super(Users, self).__init__(realm, apikey)
        self._adapter = 'users'
        self._class = 'user'

    @declassify('user')
    def by_id(self, id):
        """ lookup users by ID. returns a user. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path)

    @declassify('user')
    def by_mail(self, mail, archived=False, limit=None, page=None):
        """ lookup users by mail address.
        you may do in two ways:
            - specify one address: foo@bar.com
            - specify a domain   : @bar.com
        both will return a list.

        the role 'Zeiterfasser' may not lookup users.
        """
        path = partial(_path, self.adapter)
        if not archived:
            path = _path(self.adapter)
        else:
            path = _path(self.adapter, 'archived')
        return self._get(path, email=mail, limit=limit, page=page)

    @declassify('user')
    def all(self, archived=False, limit=None, page=None):
        """get all time entry data."""
        path = partial(_path, self.adapter)
        if not archived:
            path = _path(self.adapter)
        else:
            path = _path(self.adapter, 'archived')
        return self._get(path, limit=limit, page=page)


class TimeEntries(MiteAPI):
    """ time entries can be filtered by a lot of params:
    ids     : customer_id, project_id, service_id, user_id
    billable: true or false
    note    : note of the time entry
    locked  : true or false
    """

    def __init__(self, realm, apikey):
        super(TimeEntries, self).__init__(realm, apikey)
        self._adapter = 'time_entries'
        self._class = 'time-entry'

    @declassify('time_entry')
    def by_id(self, id):
        """ lookup time entries by ID. returns an entry. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path)

    @declassify('time_entry')
    @declassify('time_entry_group')
    def query(self, **kwargs):
        """a free query - you are responsible for the kwargs.
        Object categories 'time_entry' and 'time_entry_group' are declassed.
        See http://mite.yo.lk/en/api/time-entries.html for more information.
        """
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._get(path, **kwargs)

    @declassify('time_entry')
    def create(self, date_at=None, minutes=0, note='', user_id=None,
               project_id=None, service_id=None):
        """ date_at - date of time entry. Format YYYY-MM-DD. default: today
            minutes - default: 0
            note - default: '' (empty string)
            user_id - default: actual user id (only admin users can edit this)
            project_id - default: None
            service_id - default: None
        """
        keywords = {
            'date_at': date_at,
            'minutes': minutes,
            'note': note,
            'user_id': user_id,
            'project_id': project_id,
            'service_id': service_id,
        }
        foo = dict()
        foo['time_entry'] = keywords
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._post(path, **foo)

    def delete(self, id):
        """ delete a time entry. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._delete(path)


class Daily(MiteAPI):
    """ show daily time entries. """
    def __init__(self, realm, apikey):
        super(Daily, self).__init__(realm, apikey)
        self._adapter = 'daily'

    @declassify('time_entry')
    def at(self, year, month, day):
        """ time entries by year, month and day. """
        path = partial(_path, self.adapter)
        path = partial(path, int(year))
        path = partial(path, int(month))
        path = path(int(day))
        return self._get(path)

    @declassify('time_entry')
    def today(self):
        """ get today's entries. """
        path = _path(self.adapter)
        return self._get(path)


class Tracker(MiteAPI):
    """ show daily time entries. """
    def __init__(self, realm, apikey):
        super(Tracker, self).__init__(realm, apikey)
        self._adapter = 'tracker'

    @declassify('tracker')
    def show(self):
        """ show the state of the tracker. """
        path = _path(self.adapter)
        return self._get(path)

    @declassify('tracker')
    def start(self, id):
        """ start a specific tracker. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._put(path)

    @declassify('tracker')
    def stop(self, id):
        """ stop the tracker. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._delete(path)


# vim: set ft=python ts=4 sw=4 expandtab :
