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

from ibx_tools.logger.ibx_logger import init_logger, increase_log_level
from ibx_tools.nios.gift import Gift
from ibx_tools.nios.exceptions import WapiRequestException

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='a',
    console_log=True,
    level='info',
    max_size=100000,
    num_logs=1)

wapi = Gift()

help_text = """
Get NIOS File from member
    
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help='Infoblox Grid Manager')
@optgroup.option('-m', '--member', required=True, help='Member to retrieve file from')
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', default='admin', show_default=True, help='Infoblox admin username')
@optgroup.option(
    '-t', '--cfg-type', default='DNS_CFG', show_default=True,
    help='Configuration Type: DNS_CACHE | DNS_CFG | DHCP_CFG | DHCPV6_CFG | TRAFFIC_CAPTURE_FILE | DNS_STATS | '
         'DNS_RECURSING_CACHE'
)
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help='enable verbose debug output')
def main(grid_mgr: str, member: str, username: str, cfg_type: str, wapi_ver: str, debug: bool) -> None:
    """
    Get NIOS Configuration from Member

    Args:
        debug (bool): If True, it sets the log level to DEBUG. Default is False.
        grid_mgr (str): Manager for the wapi grid.
        member (str): Grid Member
        username (str): Username for the wapi connection.
        cfg_type (str): Configuration Type: DNS_CACHE | DNS_CFG | DHCP_CFG | DHCPV6_CFG |
                                            TRAFFIC_CAPTURE_FILE | DNS_STATS | DNS_RECURSING_CACHE
        wapi_ver (str): Version of wapi.

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
        wapi.member_config(member=member, conf_type=cfg_type)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    log.info('finished!')
    sys.exit()


if __name__ == '__main__':
    main()
