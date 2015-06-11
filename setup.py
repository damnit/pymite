#  -*- coding: utf-8 -*-
#
#  File Name: setup.py
#  Last Modified: 2014 Dez 20


__author__ = 'Daniel Altiparmak <daniel.altiparmak@inquant.de>'
__docformat__ = 'plaintext'


import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="pymite",
    version='0.1dev',
    packages=['pymite.api',
              'pymite.test',
              ],
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)


# vim: set ft=python ts=4 sw=4 expandtab :
