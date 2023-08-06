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
def reports(ctx, obj):
    """DNA Center Reports API (version: 2.2.1).

    Wraps the DNA Center Reports API and exposes the API as native Python commands.

    """
    ctx.obj = obj.reports


@reports.command()
@click.option('--view_group_id', type=str,
              help='''viewGroupId of viewgroup.''',
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
def get_views_for_a_given_view_group(obj, pretty_print, beep,
                                     view_group_id,
                                     headers):
    """Gives a list of summary of all views in a viewgroup. Use "Get all view groups" API to get the viewGroupIds (required as a query param for this API) for available viewgroups.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_views_for_a_given_view_group(
            view_group_id=view_group_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--view_group_id', type=str,
              help='''viewGroupId of viewgroup.''',
              required=True,
              show_default=True)
@click.option('--view_id', type=str,
              help='''view id of view.''',
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
def get_view_details_for_a_given_view_group_and_view(obj, pretty_print, beep,
                                                     view_group_id,
                                                     view_id,
                                                     headers):
    """Gives complete information of the view that is required to configure a report. Use "Get views for a given view group" API to get the viewIds  (required as a query param for this API) for available views.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_view_details_for_a_given_view_group_and_view(
            view_group_id=view_group_id,
            view_id=view_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--report_id', type=str,
              help='''reportId of report.''',
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
def delete_a_scheduled_report(obj, pretty_print, beep,
                              report_id,
                              headers):
    """Delete a scheduled report configuration. Deletes the report executions also.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_a_scheduled_report(
            report_id=report_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_all_view_groups(obj, pretty_print, beep,
                        headers):
    """Gives a list of summary of all view groups.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_all_view_groups(
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--view_group_id', type=str,
              help='''viewGroupId of viewgroup for report.''',
              show_default=True)
@click.option('--view_id', type=str,
              help='''viewId of view for report.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_list_of_scheduled_reports(obj, pretty_print, beep,
                                  view_group_id,
                                  view_id,
                                  headers):
    """Get list of scheduled report configurations.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_list_of_scheduled_reports(
            view_group_id=view_group_id,
            view_id=view_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--deliveries', type=str, multiple=True,
              help='''reportAPIBody's Array of available delivery channels (list of any objects).''',
              default=None,
              show_default=True)
@click.option('--name', type=str,
              help='''reportAPIBody's report name.''',
              default=None,
              show_default=True)
@click.option('--schedule', type=str,
              help='''reportAPIBody's schedule.''',
              default=None,
              show_default=True)
@click.option('--tags', type=str, multiple=True,
              help='''reportAPIBody's array of tags for report (list of string, objects).''',
              default=None,
              show_default=True)
@click.option('--view', type=str,
              help='''reportAPIBody's view.''',
              default=None,
              show_default=True)
@click.option('--viewgroupid', type=str,
              help='''reportAPIBody's viewGroupId of the viewgroup for the report.''',
              default=None,
              show_default=True)
@click.option('--viewgroupversion', type=str,
              help='''reportAPIBody's version of viewgroup for the report.''',
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
def create_or_schedule_a_report(obj, pretty_print, beep,
                                deliveries,
                                name,
                                schedule,
                                tags,
                                view,
                                viewgroupid,
                                viewgroupversion,
                                headers,
                                payload,
                                active_validation):
    """Create/Schedule a report configuration. Use "Get view details for a given view group & view" API to get the metadata required to configure a report.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        deliveries = list(deliveries)
        deliveries = json.loads('[{}]'.format(', '.join('{0}'.format(w) for w in deliveries)))
        deliveries = deliveries if len(deliveries) > 0 else None
        tags = list(tags)
        tags = json.loads('[{}]'.format(', '.join('{0}'.format(w) for w in tags)))
        tags = tags if len(tags) > 0 else None
        if view is not None:
            view = json.loads('{}'.format(view))
        result = obj.create_or_schedule_a_report(
            deliveries=deliveries,
            name=name,
            schedule=schedule,
            tags=tags,
            view=view,
            viewGroupId=viewgroupid,
            viewGroupVersion=viewgroupversion,
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


@reports.command()
@click.option('--report_id', type=str,
              help='''reportId of report.''',
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
def get_all_execution_details_for_a_given_report(obj, pretty_print, beep,
                                                 report_id,
                                                 headers):
    """Get details of all executions for a given report.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_all_execution_details_for_a_given_report(
            report_id=report_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--report_id', type=str,
              help='''reportId of report.''',
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
def get_a_scheduled_report(obj, pretty_print, beep,
                           report_id,
                           headers):
    """Get scheduled report configuration by reportId.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_a_scheduled_report(
            report_id=report_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@reports.command()
@click.option('--report_id', type=str,
              help='''reportId of report.''',
              required=True,
              show_default=True)
@click.option('--execution_id', type=str,
              help='''executionId of report execution.''',
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
def download_report_content(obj, pretty_print, beep,
                            report_id,
                            execution_id,
                            headers):
    """Returns report content. Save the response to a file by converting the response data as a blob and setting the file format available from content-disposition response header.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.download_report_content(
            report_id=report_id,
            execution_id=execution_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)
