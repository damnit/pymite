#  -*- coding: utf-8 -*-
#
#  File Name: utils.py


__author__ = 'Daniel Altiparmak <daniel.altiparmak@inquant.de>'
__docformat__ = 'plaintext'


import click
import os.path
import pkg_resources  # part of setuptools
import pathlib
import configparser


CONFIGFILE = os.path.expanduser('~/.pymite')


class Config(object):


    def __init__(self):
        self.verbose = False
        self.check = self._doesConfigFileExist()


    def _doesConfigFileExist(self):
        p = pathlib.Path(CONFIGFILE)
        try:
            with p.open() as f:
                f.close()
                return True
        except OSError:
            return False


    def createFile(self, apikey, realm):

        parser = configparser.ConfigParser()

        parser['pymite'] = {
            'realm' : realm,
            'apikey' : apikey,
        }

        with open(CONFIGFILE, 'w') as configfile:
            parser.write(configfile)

        click.echo(click.style('Config ~/.pymite created/overwritten', fg='white'))

pass_config = click.make_pass_decorator(Config, ensure=True)


# get pymite version from setuptools
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require("pymite")[0].version
    click.echo(version)
    ctx.exit()


# vim: set ft=python ts=4 sw=4 expandtab :
