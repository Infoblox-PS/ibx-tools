#!/usr/bin/env python3
"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import getpass
import sys

import click
from click_option_group import optgroup

from ibx_sdk.logger.ibx_logger import init_logger, increase_log_level
from ibx_sdk.nios.exceptions import WapiRequestException
from ibx_sdk.nios.gift import Gift

# from pkg_resources import parse_versio

__version__ = '2.0.0'

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='a',
    console_log=True,
    level='info',
    max_size=100000,
    num_logs=1
)

wapi = Gift()

help_text = """
Restore NIOS Grid.
"""


@click.command(
    help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help'])
)
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help="Infoblox NIOS Grid Manager IP/Hostname")
@optgroup.option('-f', '--filename', required=True, help="Infoblox NIOS Grid restore filename")
@optgroup.group("Optional Parameters")
@optgroup.option(
    '-u', '--username', default="admin", show_default=True, help="Infoblox NIOS username"
)
@optgroup.option(
    '-m', '--mode',
    type=click.Choice(["NORMAL", "FORCED", "CLONE"], case_sensitive=True),
    default="FORCED", show_default=True,
    help="Grid Restore Mode [NORMAL|FORCED|CLONE]"
)
@optgroup.option('-k', '--keep', is_flag=True, help="Keep existing IP otherwise use IP from backup")
@optgroup.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help='Infoblox WAPI version'
)
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help="Enable verbose logging")
def main(
        grid_mgr: str, filename: str, username: str, mode: str,
        keep: bool, wapi_ver: str,
        debug: bool
) -> None:
    """
    Restore NIOS Grid

    Args:
        mode (str): Restore Mode [NORMAL]
        debug (bool): If True, it sets the log level to DEBUG. Default is False.
        grid_mgr (str): Manager for the wapi grid.
        username (str): Username for the wapi connection.
        wapi_ver (str): Version of wapi.
        filename (str): Filename/path where the backup will be saved.
        keep: (bool): Keep existing

    Returns:
        None

    Raises:
        WapiRequestException: If unable to connect with the provided wapi parameters.
        SystemExit: The function exits the system upon completion or upon encounter of an error.

    """
    if debug:
        increase_log_level()

    wapi.grid_mgr = grid_mgr
    wapi.wapi_ver = wapi_ver
    password = getpass.getpass(
        f'Enter password for [{username}]: '
    )
    try:
        wapi.connect(username=username, password=password)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    log.info('connected to Infoblox grid manager %s', wapi.grid_mgr)

    try:
        wapi.grid_restore(
            filename=filename,
            mode=mode,
            keep_grid_ip=keep
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)


if __name__ == "__main__":
    # execute only if run as a script
    main()
