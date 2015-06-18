#  -*- coding: utf-8 -*-
#  File: utils.py
""" utils module. """


__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'


from functools import wraps


def declassify(to_remove, *args, **kwargs):
    """ flatten the return values of the mite api.
    """
    def argdecorate(fn):
        """ enable the to_remove argument to the decorator. """
        # wrap the function to get the original docstring
        @wraps(fn)
        def declassed(*args, **kwargs):
            # call the method
            ret = fn(*args, **kwargs)
            # catch errors that are thrown by the api
            try:
                # ensure that ret is a list
                if type(ret) is list:
                    return [r[to_remove] for r in ret]
                return ret[to_remove]
            except KeyError:
                return ret
        return declassed
    return argdecorate


def clean_dict(d):
    """ remove the keys with None values. """
    ktd = list()
    for k, v in d.items():
        if not v:
            ktd.append(k)
        elif type(v) is dict:
            d[k] = clean_dict(v)
    for k in ktd:
        d.pop(k)
    return d

# vim: set ft=python ts=4 sw=4 expandtab :
