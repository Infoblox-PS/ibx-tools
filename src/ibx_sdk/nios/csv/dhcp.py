import re
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import List

from pydantic import BaseModel, Field, ConfigDict, field_validator, PositiveInt

from .enums import (
    ImportActionEnum,
    LeasePerClientSettingsEnum,
    ServerAssociationTypeEnum,
    IPv6AddressTypeEnum,
    MatchOptionEnum,
    FingerprintTypeEnum,
    ProtocolTypeEnum,
    DhcpTypeEnum,
    FailoverServerType
)


class GridDhcp(BaseModel):
    model_config = ConfigDict(extra="allow")

    griddhcp: str = Field(alias="header-griddhcp", default="griddhcp")
    authority: bool | None = None
    domain_name: str | None = None
    recycle_leases: bool | None = None
    ignore_dhcp_option_list_request: bool | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    bootfile: str | None = None
    bootserver: str | None = None
    nextserver: str | None = None
    deny_bootp: bool | None = None
    enable_ddns: bool | None = None
    ddns_use_option81: bool | None = None
    ddns_server_always_updates: bool | None = None
    ddns_generate_hostname: bool | None = None
    ddns_ttl: PositiveInt | None = None
    retry_ddns_updates: bool | None = None
    ddns_retry_interval: PositiveInt | None = None  # you must set retry_ddns_updates to True to modify this
    enable_dhcp_thresholds: bool | None = None
    high_water_mark: PositiveInt | None = None
    high_water_mark_reset: PositiveInt | None = None
    low_water_mark: PositiveInt | None = None
    low_water_mark_reset: PositiveInt | None = None
    enable_email_warnings: bool | None = None
    enable_snmp_warnings: bool | None = None
    email_list: str | None = None
    ipv6_domain_name_servers: str | None = None
    ping_count: PositiveInt | None = None
    ping_timeout: PositiveInt | None = None
    capture_hostname: bool | None = None
    enable_leasequery: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    ipv6_update_dns_on_lease_renewal: bool | None = None
    txt_record_handling: str | None = None
    lease_scavenge_time: PositiveInt | None = None
    failover_port: PositiveInt | None = None
    enable_fingerprint: bool | None = None
    ipv6_enable_ddns: bool | None = None
    ipv6_enable_option_fqdn: bool | None = None
    ipv6_ddns_server_always_updates: bool | None = None
    ipv6_generate_hostname: bool | None = None
    ipv6_ddns_domainname: str | None = None
    ipv6_ddns_ttl: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    valid_lifetime: PositiveInt | None = None
    ipv6_domain_name: str | None = None
    ipv6_txt_record_handling: str | None = None
    ipv6_capture_hostname: bool | None = None
    ipv6_recycle_leases: bool | None = None
    ipv6_enable_retry_updates: bool | None = None
    ipv6_retry_updates_interval: PositiveInt | None = None
    ddns_domainname: str | None = None
    leases_per_client_settings: LeasePerClientSettingsEnum | None = None
    ignore_client_identifier: bool | None = None
    disable_all_nac_filters: bool | None = None
    format_log_option_82: str | None = None
    v6_leases_scavenging_enabled: bool | None = None
    v6_leases_scavenging_grace_period: PositiveInt | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class MemberDhcp(BaseModel):
    model_config = ConfigDict(extra="allow")

    memberdhcp: str = Field(alias="header-memberdhcp", default="memberdhcp")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    broadcast_address: IPv4Address | None
    domain_name_servers: str | None
    ignore_client_requested_options: bool | None
    pxe_lease_time: PositiveInt | None
    lease_time: PositiveInt | None
    domain_name: str | None
    routers: str | None
    option_logic_filters: str | None
    enable_pxe_lease_time: bool | None
    deny_bootp: bool | None
    bootfile: str | None
    bootserver: str | None
    nextserver: str | None
    enable_thresholds: bool | None
    range_high_water_mark: PositiveInt | None
    range_high_water_mark_reset: PositiveInt | None
    range_low_water_mark: PositiveInt | None
    range_low_water_mark_reset: PositiveInt | None
    enable_threshold_email_warnings: bool | None
    enable_threshold_snmp_warnings: bool | None
    threshold_email_addresses: str | None
    enable_ddns: bool | None
    ddns_use_option81: bool | None
    always_update_dns: bool | None
    generate_hostname: bool | None
    update_static_leases: bool | None
    ddns_ttl: PositiveInt | None
    update_dns_on_lease_renewal: bool | None
    preferred_lifetime: PositiveInt | None
    valid_lifetime: PositiveInt | None
    name: str
    is_authoritative: bool | None
    recycle_leases: bool | None
    ping_count: PositiveInt | None
    ping_timeout: PositiveInt | None
    enable_leasequery: bool | None
    retry_ddns_updates: bool | None
    ddns_retry_interval: PositiveInt | None  # you must set retry_ddns_updates to True to modify this
    lease_scavenge_time: PositiveInt | None
    enable_fingerprint: bool | None
    ipv6_enable_ddns: bool | None
    ipv6_ddns_enable_option_fqdn: bool | None
    ipv6_generate_hostname: bool | None
    ipv6_ddns_domainname: str | None
    ipv6_ddns_ttl: PositiveInt | None
    ipv6_domain_name_servers: str | None
    ipv6_domain_name: str | None
    ipv6_recycle_leases: bool | None
    ipv6_server_duid: str | None
    ipv6_enable_retry_updates: bool | None
    ipv6_retry_updates_interval: PositiveInt | None
    ipv6_update_dns_on_lease_renewal: bool | None
    ddns_domainname: str | None
    leases_per_client_settings: LeasePerClientSettingsEnum | None
    ignore_client_identifier: bool | None
    v6_leases_scavenging_enabled: bool | None
    v6_leases_scavenging_grace_period: PositiveInt | None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class NetworkView(BaseModel):
    model_config = ConfigDict(extra="allow")

    networkview: str = Field(alias="header-networkview", default="networkview")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    networkcontainer: str = Field(alias="header-networkcontainer", default="networkcontainer")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv4Address
    netmask: IPv4Address
    comment: str | None = None
    lease_time: int | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    broadcast_address: IPv4Address | None = None
    enable_ddns: bool | None = None
    ddns_domainname: str | None = None
    ddns_ttl: int | None = None
    ddns_generate_hostname: bool | None = None
    update_static_leases: bool | None = None
    enable_option81: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    enable_dhcp_thresholds: bool | None = None
    enable_email_warnings: bool | None = None
    enable_snmp_warnings: bool | None = None
    threshold_email_addresses: List[str] | None = None
    pxe_lease_time: int | None = None
    deny_bootp: bool | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    next_server: str | None = None
    option_logic_filters: str | None
    lease_scavenge_time: PositiveInt | None = None
    is_authoritative: bool | None = None
    recycle_leases: bool | None = None
    ignore_client_requested_options: bool | None = None
    network_view: str | None = None
    rir_organization: str | None = None
    rir_registration_status: str | None = None
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    remove_subnets: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class Network(BaseModel):
    model_config = ConfigDict(extra="allow")

    network: str = Field(alias="header-network", default="network")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv4Address
    netmask: IPv4Address
    rir_organization: str | None = None
    rir_registration_status: str | None = None
    network_view: str | None = None
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    comment: str | None = None
    auto_create_reversezone: bool | None = False
    is_authoritative: bool | None = None
    option_logic_filters: List[str] | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    ddns_domainname: str | None = None
    generate_hostname: bool | None = None
    always_update_dns: bool | None = None
    update_static_leases: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    ddns_ttl: int | None = None
    enable_option81: bool | None = None
    deny_bootp: bool | None = None
    broadcast_address: IPv4Address | None = None
    disabled: bool | None = None
    enable_ddns: bool | None = None
    enable_thresholds: bool | None = None
    enable_threshold_email_warnings: bool | None = None
    enable_threshold_snmp_warnings: bool | None = None
    range_high_water_mark: int | None = None
    ignore_client_requested_options: bool | None = None
    range_low_water_mark: int | None = None
    next_server: str | None = None
    lease_time: int | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: int | None = None
    recycle_leases: bool | None = None
    threshold_email_addresses: List[str] | None = None
    dhcp_members: str | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    zone_associations: List[str] | None = None  # Example: test.com/True
    vlans: str | None = None  # Example: default/1/4094/1

    # OPTION-# string where the name implies DHCP vendor class
    # OPTION-XXXX-# string where XXXX implies custom vendor class
    # ea_site: str | None = Field(alias='EA-Site', default=None)
    # EA-XXX
    # EAInherited-XXX string where ea is inherited attr
    # EA-Users string example of a user-defined attr
    # ADMGRP-XXX string example of an admin group for permissions
    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class Ipv6NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6networkcontainer: str = Field(
        alias="header-ipv6networkcontainer", default="ipv6networkcontainer"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv6Address
    cidr: PositiveInt = Field(ge=0, le=128, default=64)
    network_view: str | None = None
    comment: str | None = None
    zone_associations: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    recycle_leases: bool | None = None
    enable_ddns: bool | None = None
    ddns_domainname: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    always_update_dns: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    rir_organization: str | None = None
    rir_registration_status: str | None = None
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    remove_subnets: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class Ipv6Network(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6network: str = Field(
        alias="header-ipv6network", default="ipv6network"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv6Address
    cidr: PositiveInt = Field(ge=0, le=128, default=64)
    comment: str | None = None
    network_view: str | None = None
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    disabled: bool | None = None
    auto_create_reversezone: bool | None = False
    zone_associations: str | None = None
    dhcp_members: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    recycle_leases: bool | None = None
    enable_ddns: bool | None = None
    always_update_dns: bool | None = None
    ddns_domainname: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    vlans: str | None = None  # Example: default/1/4094/1
    rir_organization: str | None = None
    rir_registration_status: str | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited--")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class SharedNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    sharednetwork: str = Field(alias="header-sharednetwork", default="sharednetwork")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    networks: str
    network_view: str | None = None
    is_authoritative: bool | None = None
    option_logic_filters: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    comment: str | None = None
    generate_hostname: bool | None = None
    always_update_dns: bool | None = None
    update_static_leases: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    ddns_ttl: PositiveInt | None = None
    enable_option81: bool | None = None
    deny_bootp: bool | None = None
    disabled: bool | None = None
    enable_ddns: bool | None = None
    ignore_client_requested_options: bool | None = None
    next_server: str | None = None
    lease_time: PositiveInt | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6SharedNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6sharednetwork: str = Field(alias="header-ipv6sharednetwork", default="ipv6sharednetwork")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    networks: str
    network_view: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    enable_ddns: bool | None = None
    always_update_dns: bool | None = None
    ddns_domain_name: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    update_dns_on_lease_renewal: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcprange: str = Field(alias="header-dhcprange", default="dhcprange")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    start_address: IPv4Address
    new_start_address: IPv4Address | None = Field(
        alias="_new_start_address", default=None
    )
    end_address: IPv4Address
    new_end_address: IPv4Address | None = Field(alias="_new_end_address", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    is_authoritative: bool | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    ddns_domainname: str | None = None
    generate_hostname: bool | None = None
    deny_all_clients: bool | None = None
    deny_bootp: bool | None = None
    disabled: bool | None = None
    domain_name_servers: str | None = None
    enable_ddns: bool | None = None
    enable_thresholds: bool | None = None
    enable_threshold_email_warnings: bool | None = None
    enable_threshold_snmp_warnings: bool | None = None
    threshold_email_addresses: str | None = None
    range_high_water_mark: int | None = None
    ignore_client_requested_options: bool | None = None
    range_low_water_mark: int | None = None
    next_server: str | None = None
    lease_time: int | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: int | None = None
    unknown_clients_option: str | None = None  # Example: 'Allow'
    known_clients_option: str | None = None  # Example: 'Deny'
    recycle_leases: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    always_update_dns: bool | None = None
    exclusion_ranges: str | None = (
        None  # Example: “10.1.0.200-10.1.0.254/’The range for printers’,10.2.3.3-10.2.3.30/”
    )
    member: str | None = None
    server_association_type: ServerAssociationTypeEnum | None = None
    failover_association: str | None = None
    broadcast_address: IPv4Address | None = None
    routers: str | None = None
    domain_name: str | None = None
    option_logic_filters: List[str] | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6DhcpRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6dhcprange: str = Field(alias="header-ipv6dhcprange", default="ipv6dhcprange")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address_type: IPv6AddressTypeEnum | None = None
    parent: str | None = None  # Required when address_type = PREFIX
    start_address: IPv6Address
    new_start_address: IPv6Address | None = Field(alias="_new_start_address", default=None)
    end_address: IPv6Address
    new_end_address: IPv6Address | None = Field(alias="_new_end_address", default=None)
    ipv6_start_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_start_prefix: PositiveInt | None = Field(alias="_new_ipv6_start_prefix", default=None)
    ipv6_end_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_end_prefix: PositiveInt | None = Field(alias="_new_ipv6_end_prefix", default=None)
    ipv6_prefix_bits: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix_bits: PositiveInt | None = Field(alias="_new_ipv6_prefix_bits", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    member: str | None = None
    server_association_type: ServerAssociationTypeEnum | None = None
    exclusion_ranges: str | None = None
    recycle_leases: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class FixedAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    header_fixedaddress: str = Field(alias="header-fixedaddress", default="fixedaddress")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    ip_address: IPv4Address
    ms_server: IPv4Address | None = None
    new_ip_address: IPv4Address | None = Field(alias="_new_ip_address", default=None)
    network_view: str | None = None
    name: str | None = None
    always_update_dns: bool | None = None
    option_logic_filters: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    prepared_zero: bool | None = None
    comment: str | None = None
    ddns_domainname: str | None = None
    deny_bootp: bool | None = None
    broadcast_address: IPv4Address | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    dhcp_client_identifier: str | None = None
    disabled: bool | None = None
    enable_ddns: bool | None = None
    ignore_client_requested_options: bool | None = None
    circuit_id: str | None = None
    remote_id: str | None = None
    mac_address: str | None = None
    match_option: MatchOptionEnum | None = None  # MAC_ADDRESS, CLIENT_ID, CIRCUIT_ID, REMOTE_ID
    next_server: str | None = None
    lease_time: int | None = None
    enable_pxe_lease_time: bool | None = None
    ddns_hostname: str | None = None
    pxe_lease_time: int | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6FixedAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6fixedaddress: str = Field(alias="header-ipv6fixedaddress", default="ipv6fixedaddress")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address_type: IPv6AddressTypeEnum | None = None
    parent: str | None = None
    ip_address: IPv6Address
    new_ip_address: IPv6Address | None = Field(alias="_new_ip_address", default=None)
    ipv6_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix: PositiveInt | None = Field(alias="_new_ipv6_prefix", default=None)
    ipv6_prefix_bits: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix_bits: PositiveInt | None = Field(alias="_new_ipv6_prefix_bits", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    match_option: str | None = 'DUID'
    duid: str
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpFingerprint(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpfingerprint: str = Field(alias="header-dhcpfingerprint", default="dhcpfingerprint")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    type: FingerprintTypeEnum | None = Field(default=FingerprintTypeEnum.CUSTOM)
    comment: str | None = None
    disable: bool | None = None
    vendor_id: str | None = None
    option_sequence: str | None = None  # Example: "['1,3,6,7,12,15,28,40,41,42,225,226,227,22/ipv4']"
    device_class: str | None = None
    protocol: ProtocolTypeEnum

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpMacFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpmacfilter: str = Field(alias="header-dhcpmacfilter", default="dhcpmacfilter")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    never_expires: bool | None = None
    expiration_interval: PositiveInt | None = None
    enforce_expiration_time: bool | None = None
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class MacFilterAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    macfilteraddress: str = Field(
        alias="header-macfilteraddress", default="macfilteraddress"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    mac_address: str
    new_mac_address: str | None = Field(alias="_new_mac_address", default=None)
    is_registered_user: bool | None = None
    registered_user: str | None = None
    guest_first_name: str | None = None
    guest_middle_name: str | None = None
    guest_last_name: str | None = None
    guest_email: str | None = None
    guest_phone: str | None = None
    guest_custom_field1: str | None = None
    guest_custom_field2: str | None = None
    guest_custom_field3: str | None = None
    guest_custom_field4: str | None = None
    never_expires: bool | None = None
    expire_time: datetime | None = None
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class OptionFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    optionfilter: str = Field(alias="header-optionfilter", default="optionfilter")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None
    expression: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    lease_time: int | None = None
    pxe_lease_time: int | None = None
    next_server: str | None = None
    option_space: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-") or code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class OptionFilterMatchRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    optionfiltermatchrule: str = Field(
        alias="header-optionfiltermatchrule", default="optionfiltermatchrule"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    match_option: str | None = None
    match_value: str | None = None
    new_match_value: str | None = Field(alias="_new_match_value", default=None)
    comment: str | None = None
    is_substring: bool | None = None
    substring_offset: int | None = None
    substring_length: int | None = None


class RelayAgentFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    relayagentfilter: str = Field(
        alias="header-relayagentfilter", default="relayagentfilter"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None
    circuit_id_rule: str | None = None
    circuit_id: str | None = None
    remote_id_rule: str | None = None
    remote_id: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpFingerprintFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpfingerprintfilter: str = Field(
        alias="header-dhcpfingerprintfilter", default="dhcpfingerprintfilter"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    fingerprint: str | None = None
    new_fingerprint: str | None = Field(alias="_new_fingerprint", default=None)
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class OptionSpace(BaseModel):
    optionspace: str = Field(alias="header-optionspace", default="optionspace")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None

    @field_validator("name")
    def check_alphanumeric(cls, v: str) -> str:
        if not re.match(r"\w+", v):
            raise ValueError("The name of an optionspace MUST be alphanumeric.")
        return v


class Ipv6Optionspace(BaseModel):
    ipv6optionspace: str = Field(alias="header-ipv6optionspace", default="ipv6optionspace")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None
    ipv6_enterprise_number: str | None = None


class OptionDefinition(BaseModel):
    optiondefinition: str = Field(alias="header-optiondefinition", default="optiondefinition")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    space: str
    new_space: str | None = Field(alias="_new_space", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    code: str
    type: DhcpTypeEnum


class Ipv6OptionDefinition(BaseModel):
    ipv6optiondefinition: str = Field(
        alias="header-ipv6optiondefinition", default="ipv6optiondefinition"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    space: str
    new_space: str | None = Field(alias="_new_space", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    code: str
    type: DhcpTypeEnum


class DhcpFailoverAssociation(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpfailoverassociation: str = Field(
        alias="header-dhcpfailoverassociation", default="dhcpfailoverassociation"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None
    primary_server_type: FailoverServerType
    grid_primary: str | None = None
    external_primary: str | None = None
    secondary_server_type: FailoverServerType
    grid_secondary: str | None = None
    external_secondary: str | None = None
    failover_port: PositiveInt | None = Field(gt=0, lt=63999, default=647)
    max_response_delay: PositiveInt | None = Field(ge=1, default=60)
    mclt: PositiveInt | None = Field(ge=0, le=4294967295, default=3600)
    max_load_balance_delay: PositiveInt | None = Field(ge=0, le=4294967295, default=3)
    load_balance_split: PositiveInt | None = Field(ge=0, le=255, default=128)
    recycle_leases: bool | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")

