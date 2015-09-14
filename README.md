![pymite logo](https://raw.githubusercontent.com/damnit/pymite/master/docs/pymite-logo.png)

Python wrapper for the [Mite](https://mite.yo.lk) API.

[![travis](https://travis-ci.org/damnit/pymite.svg)](https://travis-ci.org/damnit/pymite) [![Coverage Status](https://coveralls.io/repos/damnit/pymite/badge.svg?branch=master&service=github)](https://coveralls.io/github/damnit/pymite?branch=master)

## Install

    pip install pymite

## Usage

    from pymite import Mite
    m = Mite("foo", "fooapikey123")
    m.tracker_adapter.show()

## backporting ##
Due to bug [1673007](https://bugs.python.org/issue1673007) in python < 3.3 we
did not plan to do a backport of pymite.
