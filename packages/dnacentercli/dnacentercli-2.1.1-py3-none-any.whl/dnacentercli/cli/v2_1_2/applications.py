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
def applications(ctx, obj):
    """DNA Center Applications API (version: 2.1.2).

    Wraps the DNA Center Applications API and exposes the API as native Python commands.

    """
    ctx.obj = obj.applications


@applications.command()
@click.option('--site_id', type=str,
              help='''Assurance site UUID value (Cannot be submitted together with deviceId and clientMac).''',
              show_default=True)
@click.option('--device_id', type=str,
              help='''Assurance device UUID value (Cannot be submitted together with siteId and clientMac).''',
              show_default=True)
@click.option('--mac_address', type=str,
              help='''Client device's MAC address (Cannot be submitted together with siteId and deviceId).''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Starting epoch time in milliseconds of time window.''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''Ending epoch time in milliseconds of time window.''',
              show_default=True)
@click.option('--application_health', type=str,
              help='''Application health category (POOR, FAIR, or GOOD.  Optionally use with siteId only).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''The offset of the first application in the returned data (optionally used with siteId only).''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The max number of application entries in returned data [1, 1000] (optionally used with siteId only).''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def applications(obj, pretty_print, beep,
                 site_id,
                 device_id,
                 mac_address,
                 start_time,
                 end_time,
                 application_health,
                 offset,
                 limit,
                 headers):
    """Intent API to get a list of applications for a specific site, a device, or a client device's MAC address.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.applications(
            site_id=site_id,
            device_id=device_id,
            mac_address=mac_address,
            start_time=start_time,
            end_time=end_time,
            application_health=application_health,
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
