#  -*- coding: utf-8 -*-
#
#  File Name: setup.py
#  Last Modified: 2014 Dez 20


__author__ = 'Daniel Altiparmak <daniel.altiparmak@inquant.de>'
__docformat__ = 'plaintext'


from setuptools import setup


setup(
    name="pymite",
    version='0.1dev',
    packages=['pymite.api',
              'pymite.cmd',
              ],
    install_requires=[
        'Click',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        pymite=pymite.cmd:cli
    '''
)

# vim: set ft=python ts=4 sw=4 expandtab :
