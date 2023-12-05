#!/usr/bin/env python3
import getpass
import sys

import click

from infoblox_pslib.nios.wapi import WAPI
from infoblox_pslib.util.ibx_logger import (
    init_logger, increase_log_level
)

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='w',
    console_log=True,
    level='info'
)
wapi = WAPI()


@click.command(
    context_settings=dict(
        max_content_width=90,
        help_option_names=['-h', '--help']
    )
)
@click.option(
    '-u', '--username', default='admin', show_default=True,
    help='Infoblox admin username'
)
@click.option(
    '-g', '--gm', required=True, help='Infoblox Grid Manager'
)
@click.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help="Infoblox WAPI version"
)
@click.option(
    '-f', '--file', required=True,
    help='Infoblox WAPI CSV export file name'
)
@click.option(
    '-o', '--object', default='network',
    help='WAPI export object type'
)
@click.option(
    '--debug', is_flag=True, help='enable verbose debug output'
)
def main(**args):
    if args.get('debug'):
        increase_log_level()
    wapi.grid_mgr = args.get('gm')
    wapi.username = args.get('username')
    wapi.wapi_ver = args.get('wapi_ver')
    wapi.password = getpass.getpass(
        f'Enter password for [{wapi.username}]: '
    )
    wapi.connect()

    wapi.csv_export(
        wapi_object=args.get('object'),
        filename=args.get('file')
    )

    sys.exit()


if __name__ == '__main__':
    main()