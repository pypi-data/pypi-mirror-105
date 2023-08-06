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
def issues(ctx, obj):
    """DNA Center Issues API (version: 2.2.1).

    Wraps the DNA Center Issues API and exposes the API as native Python commands.

    """
    ctx.obj = obj.issues


@issues.command()
@click.option('--start_time', type=int,
              help='''Starting epoch time in milliseconds of query time window.''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''Ending epoch time in milliseconds of query time window.''',
              show_default=True)
@click.option('--site_id', type=str,
              help='''Assurance UUID value of the site in the issue content.''',
              show_default=True)
@click.option('--device_id', type=str,
              help='''Assurance UUID value of the device in the issue content.''',
              show_default=True)
@click.option('--mac_address', type=str,
              help='''Client's device MAC address of the issue (format xx:xx:xx:xx:xx:xx).''',
              show_default=True)
@click.option('--priority', type=str,
              help='''The issue's priority value (One of P1, P2, P3, or P4)(Use only when macAddress and deviceId are not provided).''',
              show_default=True)
@click.option('--ai_driven', type=str,
              help='''The issue's AI driven value (Yes or No)(Use only when macAddress and deviceId are not provided).''',
              show_default=True)
@click.option('--issue_status', type=str,
              help='''The issue's status value (One of ACTIVE, IGNORED, RESOLVED) (Use only when macAddress and deviceId are not provided).''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def issues(obj, pretty_print, beep,
           start_time,
           end_time,
           site_id,
           device_id,
           mac_address,
           priority,
           ai_driven,
           issue_status,
           headers):
    """Intent API to get a list of global issues, issues for a specific device, or issue for a specific client device's MAC address.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.issues(
            start_time=start_time,
            end_time=end_time,
            site_id=site_id,
            device_id=device_id,
            mac_address=mac_address,
            priority=priority,
            ai_driven=ai_driven,
            issue_status=issue_status,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@issues.command()
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_issue_enrichment_details(obj, pretty_print, beep,
                                 headers):
    """Enriches a given network issue context (an issue id or end user’s Mac Address) with details about the issue(s), impacted hosts and suggested actions for remediation.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_issue_enrichment_details(
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)
