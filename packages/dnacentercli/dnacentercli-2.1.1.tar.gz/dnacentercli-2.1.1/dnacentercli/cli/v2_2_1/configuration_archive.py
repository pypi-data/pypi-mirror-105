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
def configuration_archive(ctx, obj):
    """DNA Center Configuration Archive API (version: 2.2.1).

    Wraps the DNA Center Configuration Archive API and exposes the API as native Python commands.

    """
    ctx.obj = obj.configuration_archive


@configuration_archive.command()
@click.option('--deviceid', type=str, multiple=True,
              help='''exportDeviceDTO's Device Id (list of strings).''',
              default=None,
              show_default=True)
@click.option('--password', type=str,
              help='''exportDeviceDTO's Password.''',
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
def export_device_configurations(obj, pretty_print, beep,
                                 deviceid,
                                 password,
                                 headers,
                                 payload,
                                 active_validation):
    """Export Device configurations to an encrypted zip file.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        deviceid = list(deviceid)
        deviceid = deviceid if len(deviceid) > 0 else None
        result = obj.export_device_configurations(
            deviceId=deviceid,
            password=password,
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
