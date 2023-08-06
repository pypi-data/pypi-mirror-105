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
def sensors(ctx, obj):
    """DNA Center Sensors API (version: 2.1.2).

    Wraps the DNA Center Sensors API and exposes the API as native Python commands.

    """
    ctx.obj = obj.sensors


@sensors.command()
@click.option('--apcoverage', type=str, multiple=True,
              help='''Ap Coverage, property of the request body (list of objects).''',
              default=None,
              show_default=True)
@click.option('--connection', type=str,
              help='''Connection, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--modelversion', type=int,
              help='''modelVersion, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--name', type=str,
              help='''Name, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--ssids', type=str, multiple=True,
              help='''Ssids, property of the request body (list of objects).''',
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
def create_sensor_test_template(obj, pretty_print, beep,
                                apcoverage,
                                connection,
                                modelversion,
                                name,
                                ssids,
                                headers,
                                payload,
                                active_validation):
    """Intent API to create a SENSOR test template with a new SSID, existing SSID, or both new and existing SSID.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        apcoverage = list(apcoverage)
        apcoverage = json.loads('[{}]'.format(', '.join('{0}'.format(w) for w in apcoverage)))
        apcoverage = apcoverage if len(apcoverage) > 0 else None
        ssids = list(ssids)
        ssids = json.loads('[{}]'.format(', '.join('{0}'.format(w) for w in ssids)))
        ssids = ssids if len(ssids) > 0 else None
        result = obj.create_sensor_test_template(
            apCoverage=apcoverage,
            connection=connection,
            modelVersion=modelversion,
            name=name,
            ssids=ssids,
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


@sensors.command()
@click.option('--template_name', type=str,
              help='''templateName query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def delete_sensor_test(obj, pretty_print, beep,
                       template_name,
                       headers):
    """Intent API to delete an existing SENSOR test template.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_sensor_test(
            template_name=template_name,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@sensors.command()
@click.option('--newtemplatename', type=str,
              help='''New Template Name, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--templatename', type=str,
              help='''Template Name, property of the request body.''',
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
def duplicate_sensor_test_template(obj, pretty_print, beep,
                                   newtemplatename,
                                   templatename,
                                   headers,
                                   payload,
                                   active_validation):
    """Intent API to duplicate an existing SENSOR test template.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.duplicate_sensor_test_template(
            newTemplateName=newtemplatename,
            templateName=templatename,
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


@sensors.command()
@click.option('--site_id', type=str,
              help='''siteId query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def sensors(obj, pretty_print, beep,
            site_id,
            headers):
    """Intent API to get a list of SENSOR devices.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.sensors(
            site_id=site_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@sensors.command()
@click.option('--locationinfolist', type=str, multiple=True,
              help='''Location Info List, property of the request body (list of objects).''',
              default=None,
              show_default=True)
@click.option('--schedule', type=str,
              help='''Schedule, property of the request body.''',
              default=None,
              show_default=True)
@click.option('--templatename', type=str,
              help='''Template Name, property of the request body.''',
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
def edit_sensor_test_template(obj, pretty_print, beep,
                              locationinfolist,
                              schedule,
                              templatename,
                              headers,
                              payload,
                              active_validation):
    """Intent API to deploy, schedule, or edit and existing SENSOR test template.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        locationinfolist = list(locationinfolist)
        locationinfolist = json.loads('[{}]'.format(', '.join('{0}'.format(w) for w in locationinfolist)))
        locationinfolist = locationinfolist if len(locationinfolist) > 0 else None
        if schedule is not None:
            schedule = json.loads('{}'.format(schedule))
        result = obj.edit_sensor_test_template(
            locationInfoList=locationinfolist,
            schedule=schedule,
            templateName=templatename,
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


@sensors.command()
@click.option('--templatename', type=str,
              help='''Template Name, property of the request body.''',
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
def run_now_sensor_test(obj, pretty_print, beep,
                        templatename,
                        headers,
                        payload,
                        active_validation):
    """Intent API to run a deployed SENSOR test.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.run_now_sensor_test(
            templateName=templatename,
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
