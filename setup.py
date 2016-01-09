#  -*- coding: utf-8 -*-
#
#  File Name: setup.py

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

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


long_description = open(os.path.join(os.path.dirname(__file__),
                        'README.txt')).read()

setup(
    name='pymite',
    version='1.0.1',
    description='Python client for Mite.yo.lk time tracking service',
    long_description=long_description,
    packages=['pymite'],
    keywords=['mite', 'pymite', 'time tracking', 'time', 'tracking',
              'mite.yo.lk'],
    author='Otto Hockel',
    author_email='hockel.otto@gmail.com',
    url='https://damnit.github.io/pymite/',
    license='MIT',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)


# vim: set ft=python ts=4 sw=4 expandtab :
