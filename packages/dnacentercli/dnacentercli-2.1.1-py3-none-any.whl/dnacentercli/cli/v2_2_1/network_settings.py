# -*- coding: utf-8 -*-
import click
import json
from ..utils.spinner import (
    init_spinner,
    start_spinner,
    stop_spinner,
)
from ..utils.print import (
    tbprint,
    eprint,
    oprint,
    opprint,
)


@click.group()
@click.pass_obj
@click.pass_context
def network_settings(ctx, obj):
    """DNA Center Network Settings API (version: 2.2.1).

    Wraps the DNA Center Network Settings API and exposes the API as native Python commands.

    """
    ctx.obj = obj.network_settings


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def update_global_pool(obj, pretty_print, beep,
                       settings,
                       headers,
                       payload,
                       active_validation):
    """API to update global pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.update_global_pool(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--id', type=str,
              help='''global pool id.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def delete_global_ip_pool(obj, pretty_print, beep,
                          id,
                          headers):
    """API to delete global IP pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_global_ip_pool(
            id=id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--id', type=str,
              help='''global credential id.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def delete_device_credential(obj, pretty_print, beep,
                             id,
                             headers):
    """Delete device credential.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_device_credential(
            id=id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--site_id', type=str,
              help='''Site id to get the network settings associated with the site.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_network(obj, pretty_print, beep,
                site_id,
                headers):
    """API to get  DHCP and DNS center server details.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_network(
            site_id=site_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--sp_profile_name', type=str,
              help='''sp profile name.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def delete_sp_profile(obj, pretty_print, beep,
                      sp_profile_name,
                      headers):
    """API to delete Service Provider profile (QoS).
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_sp_profile(
            sp_profile_name=sp_profile_name,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--site_id', type=str,
              help='''site id to get the reserve ip associated with the site.''',
              show_default=True)
@click.option('--offset', type=str,
              help='''offset/starting row.''',
              show_default=True)
@click.option('--limit', type=str,
              help='''No of Global Pools to be retrieved.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_reserve_ip_subpool(obj, pretty_print, beep,
                           site_id,
                           offset,
                           limit,
                           headers):
    """API to get the ip subpool info.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_reserve_ip_subpool(
            site_id=site_id,
            offset=offset,
            limit=limit,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def update_sp_profile(obj, pretty_print, beep,
                      settings,
                      headers,
                      payload,
                      active_validation):
    """API to update SP profile.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.update_sp_profile(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--cliid', type=str,
              help='''Cli Id, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--httpread', type=str,
              help='''Http Read, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--httpwrite', type=str,
              help='''Http Write, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--snmpv2readid', type=str,
              help='''Snmp V2 Read Id, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--snmpv2writeid', type=str,
              help='''Snmp V2 Write Id, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--snmpv3id', type=str,
              help='''Snmp V3 Id, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--site_id', type=str,
              help='''site id to assign credential.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def assign_credential_to_site(obj, pretty_print, beep,
                              cliid,
                              httpread,
                              httpwrite,
                              snmpv2readid,
                              snmpv2writeid,
                              snmpv3id,
                              site_id,
                              headers,
                              payload,
                              active_validation):
    """Assign Device Credential To Site .
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.assign_credential_to_site(
            cliId=cliid,
            httpRead=httpread,
            httpWrite=httpwrite,
            snmpV2ReadId=snmpv2readid,
            snmpV2WriteId=snmpv2writeid,
            snmpV3Id=snmpv3id,
            site_id=site_id,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def update_device_credentials(obj, pretty_print, beep,
                              settings,
                              headers,
                              payload,
                              active_validation):
    """API to update device credentials.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.update_device_credentials(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--ipv4dhcpservers', type=str, multiple=True,
              help='''IPv4 input for dhcp server ip example1.1.1.1, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv4dnsservers', type=str, multiple=True,
              help='''IPv4 input for dns server ip  example4.4.4.4, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv6addressspace', type=bool,
              help='''ipv6AddressSpace, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6dhcpservers', type=str, multiple=True,
              help='''IPv6 format dhcp server as input example 2001:db8::1234, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv6dnsservers', type=str, multiple=True,
              help='''IPv6 format dns server input example2001:db8::1234, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv6gateway', type=str,
              help='''Gateway ip address details, example2001:db8:85a3:0:100::1, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6globalpool', type=str,
              help='''IP v6 Global pool address with cidr this is required when Ipv6AddressSpace value is true, example2001:db8:85a3::/64, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6prefix', type=bool,
              help='''ipv6Prefix, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6prefixlength', type=int,
              help='''ipv6PrefixLength, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6subnet', type=str,
              help='''IPv6 Subnet address, example :2001:db8:85a3:0:100::, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6totalhost', type=int,
              help='''ipv6TotalHost, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--name', type=str,
              help='''Name of the reserve ip sub pool, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--slaacsupport', type=bool,
              help='''slaacSupport, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--id', type=str,
              help='''Id of subpool to be associated with the site.''',
              required=True,
              show_default=True)
@click.option('--site_id', type=str,
              help='''Site id of site to update sub pool.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def update_reserve_ip_subpool(obj, pretty_print, beep,
                              ipv4dhcpservers,
                              ipv4dnsservers,
                              ipv6addressspace,
                              ipv6dhcpservers,
                              ipv6dnsservers,
                              ipv6gateway,
                              ipv6globalpool,
                              ipv6prefix,
                              ipv6prefixlength,
                              ipv6subnet,
                              ipv6totalhost,
                              name,
                              slaacsupport,
                              id,
                              site_id,
                              headers,
                              payload,
                              active_validation):
    """API to update ip subpool from the global pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        ipv4dhcpservers = list(ipv4dhcpservers)
        ipv4dhcpservers = ipv4dhcpservers if len(ipv4dhcpservers) > 0 else None
        ipv4dnsservers = list(ipv4dnsservers)
        ipv4dnsservers = ipv4dnsservers if len(ipv4dnsservers) > 0 else None
        ipv6dhcpservers = list(ipv6dhcpservers)
        ipv6dhcpservers = ipv6dhcpservers if len(ipv6dhcpservers) > 0 else None
        ipv6dnsservers = list(ipv6dnsservers)
        ipv6dnsservers = ipv6dnsservers if len(ipv6dnsservers) > 0 else None
        result = obj.update_reserve_ip_subpool(
            ipv4DhcpServers=ipv4dhcpservers,
            ipv4DnsServers=ipv4dnsservers,
            ipv6AddressSpace=ipv6addressspace,
            ipv6DhcpServers=ipv6dhcpservers,
            ipv6DnsServers=ipv6dnsservers,
            ipv6GateWay=ipv6gateway,
            ipv6GlobalPool=ipv6globalpool,
            ipv6Prefix=ipv6prefix,
            ipv6PrefixLength=ipv6prefixlength,
            ipv6Subnet=ipv6subnet,
            ipv6TotalHost=ipv6totalhost,
            name=name,
            slaacSupport=slaacsupport,
            id=id,
            site_id=site_id,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--site_id', type=str,
              help='''Site id to update the network settings which is associated with the site.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def update_network(obj, pretty_print, beep,
                   settings,
                   site_id,
                   headers,
                   payload,
                   active_validation):
    """API to update network for DHCP and DNS center server settings.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.update_network(
            settings=settings,
            site_id=site_id,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--ipv4dhcpservers', type=str, multiple=True,
              help='''IPv4 input for dhcp server ip example1.1.1.1, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv4dnsservers', type=str, multiple=True,
              help='''IPv4 input for dns server ip example4.4.4.4, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv4gateway', type=str,
              help='''Gateway ip address details, example175.175.0.1, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv4globalpool', type=str,
              help='''IP v4 Global pool address with cidr, example175.175.0.0/16, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv4prefix', type=bool,
              help='''ipv4Prefix, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv4prefixlength', type=int,
              help='''ipv4PrefixLength, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv4subnet', type=str,
              help='''IPv4 Subnet address, example175.175.0.0, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv4totalhost', type=int,
              help='''ipv4TotalHost, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6addressspace', type=bool,
              help='''ipv6AddressSpace, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6dhcpservers', type=str, multiple=True,
              help='''IPv6 format dhcp server as input example 2001:db8::1234, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv6dnsservers', type=str, multiple=True,
              help='''IPv6 format dns server input example2001:db8::1234, property of the request body (list of strings).''',
              default=None,
              show_default=True)
@click.option('--ipv6gateway', type=str,
              help='''Gateway ip address details, example2001:db8:85a3:0:100::1, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6globalpool', type=str,
              help='''IPv6 Global pool address with cidr this is required when Ipv6AddressSpace value is true, example2001:db8:85a3::/64, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6prefix', type=bool,
              help='''ipv6Prefix, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6prefixlength', type=int,
              help='''ipv6PrefixLength, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6subnet', type=str,
              help='''IPv6 Subnet address, example :2001:db8:85a3:0:100::, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ipv6totalhost', type=int,
              help='''ipv6TotalHost, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--name', type=str,
              help='''Name of the reserve ip sub pool, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--slaacsupport', type=bool,
              help='''slaacSupport, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--type', type=str,
              help='''Type of the reserve ip sub pool, property of the request body. Available values are 'Generic', 'LAN', 'WAN', 'management' and 'service'.''',
              default=None,
              show_default=True)
@click.option('--site_id', type=str,
              help='''Site id to reserve the ip sub pool.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def reserve_ip_subpool(obj, pretty_print, beep,
                       ipv4dhcpservers,
                       ipv4dnsservers,
                       ipv4gateway,
                       ipv4globalpool,
                       ipv4prefix,
                       ipv4prefixlength,
                       ipv4subnet,
                       ipv4totalhost,
                       ipv6addressspace,
                       ipv6dhcpservers,
                       ipv6dnsservers,
                       ipv6gateway,
                       ipv6globalpool,
                       ipv6prefix,
                       ipv6prefixlength,
                       ipv6subnet,
                       ipv6totalhost,
                       name,
                       slaacsupport,
                       type,
                       site_id,
                       headers,
                       payload,
                       active_validation):
    """API to reserve an ip subpool from the global pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        ipv4dhcpservers = list(ipv4dhcpservers)
        ipv4dhcpservers = ipv4dhcpservers if len(ipv4dhcpservers) > 0 else None
        ipv4dnsservers = list(ipv4dnsservers)
        ipv4dnsservers = ipv4dnsservers if len(ipv4dnsservers) > 0 else None
        ipv6dhcpservers = list(ipv6dhcpservers)
        ipv6dhcpservers = ipv6dhcpservers if len(ipv6dhcpservers) > 0 else None
        ipv6dnsservers = list(ipv6dnsservers)
        ipv6dnsservers = ipv6dnsservers if len(ipv6dnsservers) > 0 else None
        result = obj.reserve_ip_subpool(
            ipv4DhcpServers=ipv4dhcpservers,
            ipv4DnsServers=ipv4dnsservers,
            ipv4GateWay=ipv4gateway,
            ipv4GlobalPool=ipv4globalpool,
            ipv4Prefix=ipv4prefix,
            ipv4PrefixLength=ipv4prefixlength,
            ipv4Subnet=ipv4subnet,
            ipv4TotalHost=ipv4totalhost,
            ipv6AddressSpace=ipv6addressspace,
            ipv6DhcpServers=ipv6dhcpservers,
            ipv6DnsServers=ipv6dnsservers,
            ipv6GateWay=ipv6gateway,
            ipv6GlobalPool=ipv6globalpool,
            ipv6Prefix=ipv6prefix,
            ipv6PrefixLength=ipv6prefixlength,
            ipv6Subnet=ipv6subnet,
            ipv6TotalHost=ipv6totalhost,
            name=name,
            slaacSupport=slaacsupport,
            type=type,
            site_id=site_id,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--site_id', type=str,
              help='''Site id to retrieve the credential details associated with the site.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_device_credential_details(obj, pretty_print, beep,
                                  site_id,
                                  headers):
    """API to get device credential details.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_device_credential_details(
            site_id=site_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--id', type=str,
              help='''Id of reserve ip subpool to be deleted.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def release_reserve_ip_subpool(obj, pretty_print, beep,
                               id,
                               headers):
    """API to delete the reserved ip subpool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.release_reserve_ip_subpool(
            id=id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_service_provider_details(obj, pretty_print, beep,
                                 headers):
    """API to get service provider details (QoS).
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_service_provider_details(
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def create_sp_profile(obj, pretty_print, beep,
                      settings,
                      headers,
                      payload,
                      active_validation):
    """API to create service provider profile(QOS).
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.create_sp_profile(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--site_id', type=str,
              help='''Site id to which site details to associate with the network settings.''',
              required=True,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def create_network(obj, pretty_print, beep,
                   settings,
                   site_id,
                   headers,
                   payload,
                   active_validation):
    """API to create a network for DHCP and DNS center server settings.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.create_network(
            settings=settings,
            site_id=site_id,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--offset', type=str,
              help='''offset/starting row.''',
              show_default=True)
@click.option('--limit', type=str,
              help='''No of Global Pools to be retrieved.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_global_pool(obj, pretty_print, beep,
                    offset,
                    limit,
                    headers):
    """API to get global pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_global_pool(
            offset=offset,
            limit=limit,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def create_device_credentials(obj, pretty_print, beep,
                              settings,
                              headers,
                              payload,
                              active_validation):
    """API to create device credentials.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.create_device_credentials(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@network_settings.command()
@click.option('--settings', type=str,
              help='''Settings, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('--payload', type=str, help='''A JSON serializable Python object to send in the body of the Request.''',
              default=None,
              show_default=True)
@click.option('--active_validation', type=bool, help='''Enable/Disable payload validation.''',
              default=True,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def create_global_pool(obj, pretty_print, beep,
                       settings,
                       headers,
                       payload,
                       active_validation):
    """API to create global pool.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        if settings is not None:
            settings = json.loads('{}'.format(settings))
        result = obj.create_global_pool(
            settings=settings,
            headers=headers,
            payload=payload,
            active_validation=active_validation)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)
