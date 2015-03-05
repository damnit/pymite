# pymite
Python Wrapper for the Mite API. PyMite also offers a self-explanatory command-line interface called pymite.

## Install

    pip install -r requirements.txt

## Command Line Tool

Pymite uses bash completion to faciliate the usage,therefore a `pymite-complete.sh` was created.

Please extend your .bashrc by adding this line:
	. /path/to/pymite-complete.sh

## pytest ##
pytest for whatever's sake does not work by just typing

    py.test -vs

you first have to cd into the test directory.

## backporting ##
Due to bug [1673007](https://bugs.python.org/issue1673007) in python < 3.3 we do
not plan to do a backport of pymite
