#  -*- coding: utf-8 -*-
#  File: mite.py
""" mite api base module"""

__author__ = 'Otto Hockel'
__docformat__ = 'plaintext'


import json
import urllib.parse
import urllib.request as request
from pymite.utils import declassify, clean_dict


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
    @declassify('account')
    def account(self):
        """ return the internal account information. """
        return self._get('account')

    @property
    @declassify('user')
    def myself(self):
        """ return the user's internal data. """
        return self._get('myself')

    def _api(self, rest):
        """ return the api in conjunction with the rest of it :). """
        return 'https://%s.mite.yo.lk/%s' % (self.realm, rest)

    def _get(self, path, **kwargs):
        """ return a dict. """
        # clean kwargs (filter None and empty string)
        clean_kwargs = clean_dict(kwargs)

        data = urllib.parse.urlencode(clean_kwargs)
        if len(data) > 0:
            api = self._api('%s.json?%s' % (path, data))
        else:
            api = self._api('%s.json' % path)
        req = request.Request(api, headers=self._headers, method='GET')

        try:
            resp = request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()

        return json.loads(resp.decode())

    def _post(self, path, **kwargs):
        """ return a dict. """
        # clean kwargs (filter None and empty string)
        clean_kwargs = clean_dict(kwargs)

        data = bytes(json.dumps(clean_kwargs), encoding='UTF-8')
        # change content type on post
        self._headers['Content-Type'] = 'application/json'
        api = self._api('%s.json' % path)
        req = request.Request(
            api, headers=self._headers, data=data, method='POST')
        try:
            resp = request.urlopen(req, data).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()
        # reset content type
        self._headers['Content-Type'] = 'text/json'
        return json.loads(resp.decode())

    def _put(self, path, **kwargs):
        """ return a dict. """
        # clean kwargs (filter None and empty string)
        clean_kwargs = clean_dict(kwargs)

        data = urllib.parse.urlencode(clean_kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
        req = request.Request(
            api, headers=self._headers, data=data, method='PUT')

        try:
            resp = request.urlopen(req).read()
        except urllib.error.HTTPError as e:
            resp = e.fp.read()

        return json.loads(resp.decode())

    def _delete(self, path, **kwargs):
        """ return a dict. """
        # clean kwargs (filter None and empty string)
        clean_kwargs = clean_dict(kwargs)

        data = urllib.parse.urlencode(clean_kwargs).encode('utf-8')
        api = self._api('%s.json' % path)
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

# vim: set ft=python ts=4 sw=4 expandtab :
