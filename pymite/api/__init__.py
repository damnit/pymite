""" mite connection library module. """

from functools import partial
from pymite.api.mite import MiteAPI
from pymite.api.utils import declassify


def _path(*args):
    return '/'.join([str(arg) for arg in args])


class DefaultReadAdapter(MiteAPI):

    def __init__(self, realm, apikey):
        super(MiteAPI, self).__init__(realm, apikey)

    def by_id(self, id):
        """get adapter data by its id."""
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path, id=id)

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
        self._class = 'project'

    @declassify('project')
    def by_id(self, id):
        return super(Projects, self).by_id(id)

    @declassify('project')
    def by_name(self, name, archived=False, limit=None, page=None):
        return super(Projects, self).by_name(archived=archived,
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
        self._class = 'service'

    @declassify('service')
    def by_id(self, id):
        return super(Services, self).by_id(id)

    @declassify('service')
    def by_name(self, name, archived=False, limit=None, page=None):
        return super(Services, self).by_name(archived=archived,
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
        self._class = 'customer'

    @declassify('customer')
    def by_id(self, id):
        return super(Customers, self).by_id(id)

    @declassify('customer')
    def by_name(self, name, archived=False, limit=None, page=None):
        return super(Customers, self).by_name(archived=archived,
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
        return self._get(path, id=id)

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
        return self._get(path, id=id)

    @declassify('time_entry')
    def from_to(self, fromdate, todate, limit=None, page=None):
        """get all time entries from date to date.
        from/to: format YYYY-MM-DD
        """
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        kws = {'from': fromdate, 'to': todate, 'limit': limit, 'page': page}
        return self._get(path, **kws)

    @declassify('time_entry')
    def at(self, at, limit=None, page=None):
        """at: today, yesterday, this_week, last_week, this_month, last_month
        or date in format YYYY-MM-DD.
        """
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._get(path, at=at, limit=limit, page=page)

    @declassify('time_entry')
    def all(self, limit=None, page=None):
        """get all time entry data."""
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._get(path, limit=limit, page=page)

    def create(self, date_at=None, minutes=0, note='', user_id=None,
               project_id=None, service_id=None):
        """ date_at - date of time entry. Format YYYY-MM-DD. default: today
            minutes - default: 0
            note - default: '' (empty string)
            user_id - default: actual user id (only admin users can edit this)
            project_id - default: None
            service_id - default: None
        """
        kwargs = {
            self._class: {
                'date_at': date_at,
                'minutes': minutes,
                'note': note,
                'user_id': user_id,
                'project_id': project_id,
                'service_id': service_id,
            }
        }
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._post(path, **kwargs)

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
        path = partial(path, year)
        path = partial(path, month)
        path = path(day)
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
        self._actual = None
        self._last = None

    @property
    def actual(self):
        return self._actual

    @property
    def last(self):
        return self._last

    @declassify('tracker')
    def show(self):
        """ show the state of the tracker. """
        path = _path(self.adapter)
        ret = self._get(path)
        # set the actual running time entry id
        try:
            self._actual = ret['tracker']['tracking_time_entry']['id']
        except KeyError:
            self._actual = None
        return ret

    @declassify('tracker')
    def start(self, id=None):
        """ start a specific tracker. """
        path = partial(_path, self.adapter)
        if not id and not self.last:
            raise Exception('No timer running')
        elif not id and self.last:
            path = path(self.last)
        else:
            path = path(id)
        ret = self._put(path)
        # set the actual running time entry id
        try:
            self._actual = ret['tracker']['tracking_time_entry']['id']
        except KeyError:
            self._actual = None
        return ret

    @declassify('tracker')
    def stop(self, id=None):
        """ stop the tracker. """
        path = partial(_path, self.adapter)
        if not id and not self.actual:
            raise Exception('No timer running')
        elif not id and self.actual:
            path = path(self.actual)
        else:
            path = path(id)
        self._last = self._actual
        self._actual = None
        return self._delete(path)


class Mite(object):
    """ API Factory that setups and returns the adapters
    """

    def __init__(self, realm, apikey):
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