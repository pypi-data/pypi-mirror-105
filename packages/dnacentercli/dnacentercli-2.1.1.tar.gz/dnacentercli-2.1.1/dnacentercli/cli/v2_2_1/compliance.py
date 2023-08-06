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
def compliance(ctx, obj):
    """DNA Center Compliance API (version: 2.2.1).

    Wraps the DNA Center Compliance API and exposes the API as native Python commands.

    """
    ctx.obj = obj.compliance


@compliance.command()
@click.option('--category', type=str,
              help='''complianceCategory can have any value among 'INTENT', 'RUNNING_CONFIG'.''',
              show_default=True)
@click.option('--compliance_type', type=str,
              help='''complianceType can have any value among 'NETWORK_DESIGN', 'NETWORK_PROFILE', 'FABRIC', 'POLICY', 'RUNNING_CONFIG'.''',
              show_default=True)
@click.option('--diff_list', type=bool,
              help='''diff list [ pass true to fetch the diff list ].''',
              show_default=True)
@click.option('--key', type=str,
              help='''extended attribute key.''',
              show_default=True)
@click.option('--value', type=str,
              help='''extended attribute value.''',
              show_default=True)
@click.option('--device_uuid', type=str,
              help='''deviceUuid path parameter.''',
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
def compliance_details_of_device(obj, pretty_print, beep,
                                 category,
                                 compliance_type,
                                 diff_list,
                                 key,
                                 value,
                                 device_uuid,
                                 headers):
    """Return compliance detailed report for a device.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.compliance_details_of_device(
            category=category,
            compliance_type=compliance_type,
            diff_list=diff_list,
            key=key,
            value=value,
            device_uuid=device_uuid,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@compliance.command()
@click.option('--device_uuid', type=str,
              help='''deviceUuid path parameter.''',
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
def device_compliance_status(obj, pretty_print, beep,
                             device_uuid,
                             headers):
    """Return compliance status of a device.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.device_compliance_status(
            device_uuid=device_uuid,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@compliance.command()
@click.option('--compliance_status', type=str,
              help='''Compliance status can be have value among 'COMPLIANT','NON_COMPLIANT','IN_PROGRESS', 'ERROR'.''',
              show_default=True)
@click.option('--device_uuid', type=str,
              help='''Comma separated deviceUuids.''',
              show_default=True)
@click.option('--offset', type=int,
              help='''offset/starting row.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''Number of records to be retrieved.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_compliance_status_(obj, pretty_print, beep,
                           compliance_status,
                           device_uuid,
                           offset,
                           limit,
                           headers):
    """Return compliance status of device(s).
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_compliance_status_(
            compliance_status=compliance_status,
            device_uuid=device_uuid,
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


@compliance.command()
@click.option('--categories', type=str, multiple=True,
              help='''POSTREQUEST's categories (list of strings).''',
              default=None,
              show_default=True)
@click.option('--deviceuuids', type=str, multiple=True,
              help='''POSTREQUEST's deviceUuids (list of strings).''',
              default=None,
              show_default=True)
@click.option('--triggerfull', type=bool,
              help='''POSTREQUEST's triggerFull.''',
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
def run_compliance(obj, pretty_print, beep,
                   categories,
                   deviceuuids,
                   triggerfull,
                   headers,
                   payload,
                   active_validation):
    """Run compliance check for device(s).
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        categories = list(categories)
        categories = categories if len(categories) > 0 else None
        deviceuuids = list(deviceuuids)
        deviceuuids = deviceuuids if len(deviceuuids) > 0 else None
        result = obj.run_compliance(
            categories=categories,
            deviceUuids=deviceuuids,
            triggerFull=triggerfull,
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
