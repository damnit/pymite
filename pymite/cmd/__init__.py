#  -*- coding: utf-8 -*-
#
#  File Name: pymite.py
#  Creation Date: 2012 Jul 24
#  Last Modified: 2014 Dez 19


__author__ = 'Daniel Altiparmak <daniel.altiparmak@inquant.de>'
__docformat__ = 'plaintext'


import click

try:
    range_type = xrange
except NameError:
    range_type = range


class Config(object):

    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def cli(config, verbose):
    config.verbose = verbose


@cli.command()
@click.argument('name')
@click.argument('api_key')
@pass_config
def configure(config, name, api_key):
    '''configure your account to use pymite.
    This creates a .pymite file in your home folder.
    If file already exists, those config options get overwritten
    '''
    if config.verbose:
        click.echo('We are in verbose mode')
    click.echo(name)
    click.echo(api_key)

# vim: set ft=python ts=4 sw=4 expandtab :

