""" mite connection library module. """

import json
import urllib.request as request
import urllib.parse
import urllib.error
from functools import partial


def _path(*args):
    return '/'.join([str(arg) for arg in args])


class MiteAPI(object):
    """ wrap the mite api. """

    def __init__(self, realm, apikey):
        self._realm = realm
        self._apikey = apikey
        self._headers = {
            'X-MiteApiKey': apikey,
            'Content-Type': 'text/json',
            'User-Agent': 'pymite/dev (https://github.com/damnit)'
        }
        self._api = partial(_path, 'https://%s.mite.yo.lk' % realm)

    def __repr__(self):
        return '<mite: %s Adapter>' % (self.__class__.__name__)

    @property
    def realm(self):
        return self._realm

    @property
    def adapter(self):
        return self._adapter

    @property
    def apikey(self):
        return self._apikey

    @property
    def account(self):
        """ return the user's internal data. """
        return self._get('account')

    @property
    def myself(self):
        """ return the user's internal data. """
        return self._get('myself')

    def api(self, realm, rest):
        """ return the api in conjunction with the rest of it :). """
        return 'https://%s.mite.yo.lk/%s' % (realm, rest)

    def _get(self, path, **kwargs):
        """ return a dict. """
        # remove None values with new python 3 dict comprehension
        kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}

        data = urllib.parse.urlencode(kwargs)

        api = self.api(self.realm, '%s.json?%s' % (path, data))
        req = request.Request(api, headers=self._headers, method='GET')

        try:
            resp = request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()

        return json.loads(resp.decode())

    def _put(self, path, **kwargs):
        """ return a dict. """
        kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}

        data = urllib.parse.urlencode(kwargs).encode('utf-8')

        api = self.api(self.realm, '%s.json' % (path))
        req = request.Request(
            api, headers=self._headers, data=data, method='PUT')

        try:
            resp = request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()

        return json.loads(resp.decode())

    def _delete(self, path, **kwargs):
        """ return a dict. """
        kwargs = {k: v for k, v in kwargs.items() if v is not '' or None}

        data = urllib.parse.urlencode(kwargs).encode('utf-8')

        api = self.api(self.realm, '%s.json' % (path))
        req = request.Request(
            api, headers=self._headers, data=data, method='DELETE')

        try:
            resp = request.urlopen(req)
            resp_txt = resp.read().strip()
            # TODO: is this right? The Mite API returns b' ' in this case
            if resp.code == 200 and not resp_txt:
                resp = b'{"success": 200}'
            else:
                resp = resp_txt
        except urllib.error.HTTPError as e:
            resp = e.fp.read()
        return json.loads(resp.decode())

    def _post(self, path, **kwargs):
        """ return a dict. """
        kwargs = {k: v for k, v in kwargs.items() if v is not ('' or None)}

        data = bytes(json.dumps(kwargs), encoding='UTF-8')
        # change content type on post
        self._headers['Content-Type'] = 'application/json'
        api = self.api(self.realm, '%s.json' % (path))
        req = request.Request(
            api, headers=self._headers, data=data, method='POST')
        try:
            resp = request.urlopen(req, data).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()
        # reset content type
        self._headers['Content-Type'] = 'text/json'
        return json.loads(resp.decode())


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


class Services(DefaultReadAdapter):
    """ the services class. """

    def __init__(self, realm, apikey):
        super(DefaultReadAdapter, self).__init__(realm, apikey)
        self._adapter = 'services'
        self._class = 'service'


class Customers(DefaultReadAdapter):
    """ the customers class. """

    def __init__(self, realm, apikey):
        super(DefaultReadAdapter, self).__init__(realm, apikey)
        self._adapter = 'customers'
        self._class = 'customer'


class Users(MiteAPI):
    """ the users class. """

    def __init__(self, realm, apikey):
        super(Users, self).__init__(realm, apikey)
        self._adapter = 'users'
        self._class = 'user'

    def by_id(self, id):
        """ lookup users by ID. returns a user. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path, id=id)

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

    def by_id(self, id):
        """ lookup time entries by ID. returns an entry. """
        path = partial(_path, self.adapter)
        path = path(id)
        return self._get(path, id=id)

    def from_to(self, fromdate, todate, limit=None, page=None):
        """get all time entries from date to date.
        from/to: format YYYY-MM-DD
        """
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        kws = {'from': fromdate, 'to': todate, 'limit': limit, 'page': page}
        return self._get(path, **kws)

    def at(self, at, limit=None, page=None):
        """at: today, yesterday, this_week, last_week, this_month, last_month
        or date in format YYYY-MM-DD.
        """
        path = partial(_path, self.adapter)
        path = _path(self.adapter)
        return self._get(path, at=at, limit=limit, page=page)

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

    def at(self, year, month, day):
        """ time entries by year, month and day. """
        path = partial(_path, self.adapter)
        path = partial(path, year)
        path = partial(path, month)
        path = path(day)
        return self._get(path)

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
