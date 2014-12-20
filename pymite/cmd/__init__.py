#  -*- coding: utf-8 -*-
#
#  File Name: __init__.py
#  Last Modified: 2014 Dez 20


__author__ = 'Daniel Altiparmak <daniel.altiparmak@inquant.de>'
__docformat__ = 'plaintext'


from pymite.cmd.utils import pass_config
from pymite.cmd.utils import print_version
import click
import os


try:
    range_type = xrange
except NameError:
    range_type = range


@click.group()
@click.option('--verbose', '-v', is_flag=True)
@click.option('--version', '-V', is_flag=True,
              callback=print_version,
              expose_value=False, is_eager=True)
@pass_config
@click.pass_context
def cli(ctx, config, verbose):
    config.verbose = verbose

    # check for all subcommands if config file exists
    # don't check if we are in configure context
    if ctx.invoked_subcommand != 'configure':
        if config.check is False:
            raise click.UsageError('No config file exists. Please create one, '\
                                'by calling "pymite configure" subcommand ',
                                ctx=None)


@cli.command()
@click.option('--apikey','-a',
              type=click.STRING,
              required=True,
              help='Login to http://mite.yo.lk/api/index.html' \
                   'and create your API Key')
@click.option('--realm','-r',
              help='realm is the part in the URL: https://<realm>.mite.yo.lk',
              type=click.STRING,
              required=True)
@pass_config
def configure(config, apikey, realm):
    '''configure your account to use pymite.
    This creates a .pymite file in your home folder.
    If file already exists, those config options get overwritten
    '''
    if config.verbose:
        click.echo('We are in verbose mode')

    config.createFile(apikey, realm)



@cli.command()
@pass_config
def test(config):
    '''TEST
    '''
    if config.verbose:
        click.echo('We are in verbose mode')
    click.echo("in test")


# vim: set ft=python ts=4 sw=4 expandtab :

