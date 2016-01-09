.. figure:: https://raw.githubusercontent.com/damnit/pymite/master/docs/pymite-logo.png
   :alt: pymite logo

   pymite logo

Python wrapper for the `Mite`_ API.

|travis| |Coverage Status|

Install
-------

::

    pip install pymite

Usage
-----

::

    from pymite import Mite
    m = Mite("foo", "fooapikey123")
    m.tracker_adapter.show()

backporting
-----------

Due to bug `1673007`_ in python < 3.3 we did not plan to do a backport
of pymite.

.. _Mite: https://mite.yo.lk
.. _1673007: https://bugs.python.org/issue1673007

.. |travis| image:: https://travis-ci.org/damnit/pymite.svg
   :target: https://travis-ci.org/damnit/pymite
.. |Coverage Status| image:: https://coveralls.io/repos/damnit/pymite/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/damnit/pymite?branch=master
