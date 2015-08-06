![pymite logo](https://raw.githubusercontent.com/damnit/pymite/master/docs/pymite-logo.png)
Python wrapper for the [Mite](https://mite.yo.lk) API.

## Install

    pip install pymite

## Usage

    from pymite.api import Mite
    m = Mite("foo", "fooapikey123")
    m.tracker_adapter.show()

## backporting ##
Due to bug [1673007](https://bugs.python.org/issue1673007) in python < 3.3 we do
not plan to do a backport of pymite
