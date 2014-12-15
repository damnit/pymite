""" mite cli - use this with python 3.x.
This is really a TODO as it only jumps into a ipython shell.

The plan is to use cmd.Cmd as a generic and stdlib module.
"""

import sys
from mite import Mite

APIKEY = 'flirz123'

if __name__ == '__main__':
    try:
        APIKEY = sys.argv[1]
    except KeyError:
        print('Please provide your mite apikey as parameter.')
        exit(-1)
    m = Mite('inquant', APIKEY)
    from IPython import embed; embed()

# vim: set ft=python ts=4 sw=4 expandtab :
