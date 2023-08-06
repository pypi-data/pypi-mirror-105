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
def event_management(ctx, obj):
    """DNA Center Event Management API (version: 2.2.1).

    Wraps the DNA Center Event Management API and exposes the API as native Python commands.

    """
    ctx.obj = obj.event_management


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of subscriptions related to the respective eventIds.''',
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
def count_of_event_subscriptions(obj, pretty_print, beep,
                                 event_ids,
                                 headers):
    """Returns the Count of EventSubscriptions.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.count_of_event_subscriptions(
            event_ids=event_ids,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_ids', type=str,
              help='''The registered EventId should be provided.''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Start Time in milliseconds.''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''End Time in milliseconds.''',
              show_default=True)
@click.option('--category', type=str,
              help='''category query parameter.''',
              show_default=True)
@click.option('--type', type=str,
              help='''type query parameter.''',
              show_default=True)
@click.option('--severity', type=str,
              help='''severity query parameter.''',
              show_default=True)
@click.option('--domain', type=str,
              help='''domain query parameter.''',
              show_default=True)
@click.option('--sub_domain', type=str,
              help='''Sub Domain.''',
              show_default=True)
@click.option('--source', type=str,
              help='''source query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def count_of_notifications(obj, pretty_print, beep,
                           event_ids,
                           start_time,
                           end_time,
                           category,
                           type,
                           severity,
                           domain,
                           sub_domain,
                           source,
                           headers):
    """Get the Count of Published Notifications.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.count_of_notifications(
            event_ids=event_ids,
            start_time=start_time,
            end_time=end_time,
            category=category,
            type=type,
            severity=severity,
            domain=domain,
            sub_domain=sub_domain,
            source=source,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--connector_type', type=str,
              help='''Connector Type [SYSLOG].''',
              required=True,
              show_default=True)
@click.option('--name', type=str,
              help='''Name of the specific configuration.''',
              show_default=True)
@click.option('--instance_id', type=str,
              help='''Instance Id of the specific configuration.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_syslog_subscription_details(obj, pretty_print, beep,
                                    connector_type,
                                    name,
                                    instance_id,
                                    headers):
    """Gets the list of subscription details for specified connectorType.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_syslog_subscription_details(
            connector_type=connector_type,
            name=name,
            instance_id=instance_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--connector_type', type=str,
              help='''Connector Type [EMAIL].''',
              required=True,
              show_default=True)
@click.option('--name', type=str,
              help='''Name of the specific configuration.''',
              show_default=True)
@click.option('--instance_id', type=str,
              help='''Instance Id of the specific configuration.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_email_subscription_details(obj, pretty_print, beep,
                                   connector_type,
                                   name,
                                   instance_id,
                                   headers):
    """Gets the list of subscription details for specified connectorType.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_email_subscription_details(
            connector_type=connector_type,
            name=name,
            instance_id=instance_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of email subscriptions related to the respective eventIds (Comma separated event ids).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''The number of Subscriptions's to offset in the resultset whose default value 0.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The number of Subscriptions's to limit in the resultset whose default value 10.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''SortBy field name.''',
              show_default=True)
@click.option('--order', type=str,
              help='''order query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_email_event_subscriptions(obj, pretty_print, beep,
                                  event_ids,
                                  offset,
                                  limit,
                                  sort_by,
                                  order,
                                  headers):
    """Gets the list of email Subscriptions's based on provided offset and limit.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_email_event_subscriptions(
            event_ids=event_ids,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_id', type=str,
              help='''The registered EventId should be provided.''',
              show_default=True)
@click.option('--tags', type=str,
              help='''The registered Tags should be provided.''',
              required=True,
              show_default=True)
@click.option('--offset', type=int,
              help='''The number of Registries to offset in the resultset whose default value 0.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The number of Registries to limit in the resultset whose default value 10.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''SortBy field name.''',
              show_default=True)
@click.option('--order', type=str,
              help='''order query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_events(obj, pretty_print, beep,
               event_id,
               tags,
               offset,
               limit,
               sort_by,
               order,
               headers):
    """Gets the list of registered Events with provided eventIds or tags as mandatory.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_events(
            event_id=event_id,
            tags=tags,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--parent_instance_id', type=str,
              help='''Parent Audit Log record's instanceID.''',
              show_default=True)
@click.option('--is_parent_only', type=bool,
              help='''Parameter to filter parent only audit-logs.''',
              show_default=True)
@click.option('--instance_id', type=str,
              help='''InstanceID of the Audit Log.''',
              show_default=True)
@click.option('--name', type=str,
              help='''Audit Log notification event name.''',
              show_default=True)
@click.option('--event_id', type=str,
              help='''Audit Log notification's event ID. .''',
              show_default=True)
@click.option('--category', type=str,
              help='''Audit Log notification's event category. Supported valuesINFO, WARN, ERROR, ALERT, TASK_PROGRESS, TASK_FAILURE, TASK_COMPLETE, COMMAND, QUERY, CONVERSATION.''',
              show_default=True)
@click.option('--severity', type=str,
              help='''Audit Log notification's event severity. Supported values1, 2, 3, 4, 5.''',
              show_default=True)
@click.option('--domain', type=str,
              help='''Audit Log notification's event domain.''',
              show_default=True)
@click.option('--sub_domain', type=str,
              help='''Audit Log notification's event sub-domain.''',
              show_default=True)
@click.option('--source', type=str,
              help='''Audit Log notification's event source.''',
              show_default=True)
@click.option('--user_id', type=str,
              help='''Audit Log notification's event userId.''',
              show_default=True)
@click.option('--context', type=str,
              help='''Audit Log notification's event correlationId.''',
              show_default=True)
@click.option('--event_hierarchy', type=str,
              help='''Audit Log notification's event eventHierarchy. Example"US.CA.San Jose" OR "US.CA" OR "CA.San Jose" - Delimiter for hierarchy separation is ".".''',
              show_default=True)
@click.option('--site_id', type=str,
              help='''Audit Log notification's siteId.''',
              show_default=True)
@click.option('--device_id', type=str,
              help='''Audit Log notification's deviceId.''',
              show_default=True)
@click.option('--is_system_events', type=bool,
              help='''Parameter to filter system generated audit-logs.''',
              show_default=True)
@click.option('--description', type=str,
              help='''String full/partial search - (Provided input string is case insensitively matched for records).''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Start Time in milliseconds since Epoch Eg. 1597950637211 (when provided endTime is mandatory).''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''End Time in milliseconds since Epoch Eg. 1597961437211 (when provided startTime is mandatory).''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_auditlog_summary(obj, pretty_print, beep,
                         parent_instance_id,
                         is_parent_only,
                         instance_id,
                         name,
                         event_id,
                         category,
                         severity,
                         domain,
                         sub_domain,
                         source,
                         user_id,
                         context,
                         event_hierarchy,
                         site_id,
                         device_id,
                         is_system_events,
                         description,
                         start_time,
                         end_time,
                         headers):
    """Get Audit Log Summary from the Event-Hub.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_auditlog_summary(
            parent_instance_id=parent_instance_id,
            is_parent_only=is_parent_only,
            instance_id=instance_id,
            name=name,
            event_id=event_id,
            category=category,
            severity=severity,
            domain=domain,
            sub_domain=sub_domain,
            source=source,
            user_id=user_id,
            context=context,
            event_hierarchy=event_hierarchy,
            site_id=site_id,
            device_id=device_id,
            is_system_events=is_system_events,
            description=description,
            start_time=start_time,
            end_time=end_time,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
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
def create_event_subscriptions(obj, pretty_print, beep,
                               headers,
                               payload,
                               active_validation):
    """Subscribe SubscriptionEndpoint to list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.create_event_subscriptions(
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


@event_management.command()
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
def update_event_subscriptions(obj, pretty_print, beep,
                               headers,
                               payload,
                               active_validation):
    """Update SubscriptionEndpoint to list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.update_event_subscriptions(
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


@event_management.command()
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
def update_syslog_event_subscription(obj, pretty_print, beep,
                                     headers,
                                     payload,
                                     active_validation):
    """Update Syslog Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.update_syslog_event_subscription(
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


@event_management.command()
@click.option('--event_id', type=str,
              help='''The registered EventId should be provided.''',
              show_default=True)
@click.option('--tags', type=str,
              help='''The registered Tags should be provided.''',
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
def count_of_events(obj, pretty_print, beep,
                    event_id,
                    tags,
                    headers):
    """Get the count of registered events with provided eventIds or tags as mandatory.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.count_of_events(
            event_id=event_id,
            tags=tags,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of eventIds.''',
              show_default=True)
@click.option('--tags', type=str,
              help='''Tags defined.''',
              show_default=True)
@click.option('--offset', type=int,
              help='''Record start offset.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''# of records to return in result set.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''Sort by field.''',
              show_default=True)
@click.option('--order', type=str,
              help='''sorting order (asc/desc).''',
              show_default=True)
@click.option('--search', type=str,
              help='''findd matches in name, description, eventId, type, category.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_eventartifacts(obj, pretty_print, beep,
                       event_ids,
                       tags,
                       offset,
                       limit,
                       sort_by,
                       order,
                       search,
                       headers):
    """Gets the list of artifacts based on provided offset and limit.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_eventartifacts(
            event_ids=event_ids,
            tags=tags,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            search=search,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
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
def create_email_event_subscription(obj, pretty_print, beep,
                                    headers,
                                    payload,
                                    active_validation):
    """Create Email Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.create_email_event_subscription(
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


@event_management.command()
@click.option('--event_ids', type=str,
              help='''The registered EventId should be provided.''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Start Time in milliseconds.''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''End Time in milliseconds.''',
              show_default=True)
@click.option('--category', type=str,
              help='''category query parameter.''',
              show_default=True)
@click.option('--type', type=str,
              help='''type query parameter.''',
              show_default=True)
@click.option('--severity', type=str,
              help='''severity query parameter.''',
              show_default=True)
@click.option('--domain', type=str,
              help='''domain query parameter.''',
              show_default=True)
@click.option('--sub_domain', type=str,
              help='''Sub Domain.''',
              show_default=True)
@click.option('--source', type=str,
              help='''source query parameter.''',
              show_default=True)
@click.option('--offset', type=int,
              help='''Start Offset.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''# of records.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''Sort By column.''',
              show_default=True)
@click.option('--order', type=str,
              help='''Ascending/Descending order [asc/desc].''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_notifications(obj, pretty_print, beep,
                      event_ids,
                      start_time,
                      end_time,
                      category,
                      type,
                      severity,
                      domain,
                      sub_domain,
                      source,
                      offset,
                      limit,
                      sort_by,
                      order,
                      headers):
    """Get the list of Published Notifications.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_notifications(
            event_ids=event_ids,
            start_time=start_time,
            end_time=end_time,
            category=category,
            type=type,
            severity=severity,
            domain=domain,
            sub_domain=sub_domain,
            source=source,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--parent_instance_id', type=str,
              help='''Parent Audit Log record's instanceID.''',
              show_default=True)
@click.option('--instance_id', type=str,
              help='''InstanceID of the Audit Log.''',
              show_default=True)
@click.option('--name', type=str,
              help='''Audit Log notification event name.''',
              show_default=True)
@click.option('--event_id', type=str,
              help='''Audit Log notification's event ID. .''',
              show_default=True)
@click.option('--category', type=str,
              help='''Audit Log notification's event category. Supported valuesINFO, WARN, ERROR, ALERT, TASK_PROGRESS, TASK_FAILURE, TASK_COMPLETE, COMMAND, QUERY, CONVERSATION.''',
              show_default=True)
@click.option('--severity', type=str,
              help='''Audit Log notification's event severity. Supported values1, 2, 3, 4, 5.''',
              show_default=True)
@click.option('--domain', type=str,
              help='''Audit Log notification's event domain.''',
              show_default=True)
@click.option('--sub_domain', type=str,
              help='''Audit Log notification's event sub-domain.''',
              show_default=True)
@click.option('--source', type=str,
              help='''Audit Log notification's event source.''',
              show_default=True)
@click.option('--user_id', type=str,
              help='''Audit Log notification's event userId.''',
              show_default=True)
@click.option('--context', type=str,
              help='''Audit Log notification's event correlationId.''',
              show_default=True)
@click.option('--event_hierarchy', type=str,
              help='''Audit Log notification's event eventHierarchy. Example"US.CA.San Jose" OR "US.CA" OR "CA.San Jose" - Delimiter for hierarchy separation is ".".''',
              show_default=True)
@click.option('--site_id', type=str,
              help='''Audit Log notification's siteId.''',
              show_default=True)
@click.option('--device_id', type=str,
              help='''Audit Log notification's deviceId.''',
              show_default=True)
@click.option('--is_system_events', type=bool,
              help='''Parameter to filter system generated audit-logs.''',
              show_default=True)
@click.option('--description', type=str,
              help='''String full/partial search - (Provided input string is case insensitively matched for records).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''Position of a particular Audit Log record in the data. .''',
              show_default=True)
@click.option('--limit', type=int,
              help='''Number of Audit Log records to be returned per page.''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Start Time in milliseconds since Epoch Eg. 1597950637211 (when provided endTime is mandatory).''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''End Time in milliseconds since Epoch Eg. 1597961437211 (when provided startTime is mandatory).''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''Sort the Audit Logs by certain fields. Supported values are event notification header attributes.''',
              show_default=True)
@click.option('--order', type=str,
              help='''Order of the sorted Audit Log records. Default value is desc by timestamp. Supported valuesasc, desc.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_auditlog_records(obj, pretty_print, beep,
                         parent_instance_id,
                         instance_id,
                         name,
                         event_id,
                         category,
                         severity,
                         domain,
                         sub_domain,
                         source,
                         user_id,
                         context,
                         event_hierarchy,
                         site_id,
                         device_id,
                         is_system_events,
                         description,
                         offset,
                         limit,
                         start_time,
                         end_time,
                         sort_by,
                         order,
                         headers):
    """Get Audit Log Event instances from the Event-Hub .
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_auditlog_records(
            parent_instance_id=parent_instance_id,
            instance_id=instance_id,
            name=name,
            event_id=event_id,
            category=category,
            severity=severity,
            domain=domain,
            sub_domain=sub_domain,
            source=source,
            user_id=user_id,
            context=context,
            event_hierarchy=event_hierarchy,
            site_id=site_id,
            device_id=device_id,
            is_system_events=is_system_events,
            description=description,
            offset=offset,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
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
def create_syslog_event_subscription(obj, pretty_print, beep,
                                     headers,
                                     payload,
                                     active_validation):
    """Create Syslog Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.create_syslog_event_subscription(
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


@event_management.command()
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
def update_email_event_subscription(obj, pretty_print, beep,
                                    headers,
                                    payload,
                                    active_validation):
    """Update Email Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.update_email_event_subscription(
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


@event_management.command()
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
def create_rest_webhook_event_subscription(obj, pretty_print, beep,
                                           headers,
                                           payload,
                                           active_validation):
    """Create Rest/Webhook Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.create_rest_webhook_event_subscription(
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


@event_management.command()
@click.option('--subscriptions', type=str,
              help='''List of EventSubscriptionId's for removal.''',
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
def delete_event_subscriptions(obj, pretty_print, beep,
                               subscriptions,
                               headers):
    """Delete EventSubscriptions.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.delete_event_subscriptions(
            subscriptions=subscriptions,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--instance_id', type=str,
              help='''InstanceID of the Audit Log.''',
              show_default=True)
@click.option('--name', type=str,
              help='''Audit Log notification event name.''',
              show_default=True)
@click.option('--event_id', type=str,
              help='''Audit Log notification's event ID. .''',
              show_default=True)
@click.option('--category', type=str,
              help='''Audit Log notification's event category. Supported valuesINFO, WARN, ERROR, ALERT, TASK_PROGRESS, TASK_FAILURE, TASK_COMPLETE, COMMAND, QUERY, CONVERSATION.''',
              show_default=True)
@click.option('--severity', type=str,
              help='''Audit Log notification's event severity. Supported values1, 2, 3, 4, 5.''',
              show_default=True)
@click.option('--domain', type=str,
              help='''Audit Log notification's event domain.''',
              show_default=True)
@click.option('--sub_domain', type=str,
              help='''Audit Log notification's event sub-domain.''',
              show_default=True)
@click.option('--source', type=str,
              help='''Audit Log notification's event source.''',
              show_default=True)
@click.option('--user_id', type=str,
              help='''Audit Log notification's event userId.''',
              show_default=True)
@click.option('--context', type=str,
              help='''Audit Log notification's event correlationId.''',
              show_default=True)
@click.option('--event_hierarchy', type=str,
              help='''Audit Log notification's event eventHierarchy. Example"US.CA.San Jose" OR "US.CA" OR "CA.San Jose" - Delimiter for hierarchy separation is ".".''',
              show_default=True)
@click.option('--site_id', type=str,
              help='''Audit Log notification's siteId.''',
              show_default=True)
@click.option('--device_id', type=str,
              help='''Audit Log notification's deviceId.''',
              show_default=True)
@click.option('--is_system_events', type=bool,
              help='''Parameter to filter system generated audit-logs.''',
              show_default=True)
@click.option('--description', type=str,
              help='''String full/partial search - (Provided input string is case insensitively matched for records).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''Position of a particular Audit Log record in the data. .''',
              show_default=True)
@click.option('--limit', type=int,
              help='''Number of Audit Log records to be returned per page.''',
              show_default=True)
@click.option('--start_time', type=int,
              help='''Start Time in milliseconds since Epoch Eg. 1597950637211 (when provided endTime is mandatory).''',
              show_default=True)
@click.option('--end_time', type=int,
              help='''End Time in milliseconds since Epoch Eg. 1597961437211 (when provided startTime is mandatory).''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''Sort the Audit Logs by certain fields. Supported values are event notification header attributes.''',
              show_default=True)
@click.option('--order', type=str,
              help='''Order of the sorted Audit Log records. Default value is desc by timestamp. Supported valuesasc, desc.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_auditlog_parent_records(obj, pretty_print, beep,
                                instance_id,
                                name,
                                event_id,
                                category,
                                severity,
                                domain,
                                sub_domain,
                                source,
                                user_id,
                                context,
                                event_hierarchy,
                                site_id,
                                device_id,
                                is_system_events,
                                description,
                                offset,
                                limit,
                                start_time,
                                end_time,
                                sort_by,
                                order,
                                headers):
    """Get Parent Audit Log Event instances from the Event-Hub .
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_auditlog_parent_records(
            instance_id=instance_id,
            name=name,
            event_id=event_id,
            category=category,
            severity=severity,
            domain=domain,
            sub_domain=sub_domain,
            source=source,
            user_id=user_id,
            context=context,
            event_hierarchy=event_hierarchy,
            site_id=site_id,
            device_id=device_id,
            is_system_events=is_system_events,
            description=description,
            offset=offset,
            limit=limit,
            start_time=start_time,
            end_time=end_time,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def eventartifact_count(obj, pretty_print, beep,
                        headers):
    """Get the count of registered event artifacts with provided eventIds or tags as mandatory.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.eventartifact_count(
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of subscriptions related to the respective eventIds (Comma separated event ids).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''The number of Subscriptions's to offset in the resultset whose default value 0.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The number of Subscriptions's to limit in the resultset whose default value 10.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''SortBy field name.''',
              show_default=True)
@click.option('--order', type=str,
              help='''order query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_rest_webhook_event_subscriptions(obj, pretty_print, beep,
                                         event_ids,
                                         offset,
                                         limit,
                                         sort_by,
                                         order,
                                         headers):
    """Gets the list of Rest/Webhook Subscriptions's based on provided offset and limit.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_rest_webhook_event_subscriptions(
            event_ids=event_ids,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of subscriptions related to the respective eventIds (Comma separated event ids).''',
              show_default=True)
@click.option('--offset', type=int,
              help='''The number of Subscriptions's to offset in the resultset whose default value 0.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The number of Subscriptions's to limit in the resultset whose default value 10.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''SortBy field name.''',
              show_default=True)
@click.option('--order', type=str,
              help='''order query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_syslog_event_subscriptions(obj, pretty_print, beep,
                                   event_ids,
                                   offset,
                                   limit,
                                   sort_by,
                                   order,
                                   headers):
    """Gets the list of Syslog Subscriptions's based on provided offset and limit.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_syslog_event_subscriptions(
            event_ids=event_ids,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--connector_type', type=str,
              help='''Connector Type [REST].''',
              required=True,
              show_default=True)
@click.option('--name', type=str,
              help='''Name of the specific configuration.''',
              show_default=True)
@click.option('--instance_id', type=str,
              help='''Instance Id of the specific configuration.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_rest_webhook_subscription_details(obj, pretty_print, beep,
                                          connector_type,
                                          name,
                                          instance_id,
                                          headers):
    """Gets the list of subscription details for specified connectorType.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_rest_webhook_subscription_details(
            connector_type=connector_type,
            name=name,
            instance_id=instance_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
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
def update_rest_webhook_event_subscription(obj, pretty_print, beep,
                                           headers,
                                           payload,
                                           active_validation):
    """Update Rest/Webhook Subscription Endpoint for list of registered events.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        if payload is not None:
            payload = json.loads(payload)
        result = obj.update_rest_webhook_event_subscription(
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


@event_management.command()
@click.option('--event_ids', type=str,
              help='''List of subscriptions related to the respective eventIds.''',
              show_default=True)
@click.option('--offset', type=int,
              help='''The number of Subscriptions's to offset in the resultset whose default value 0.''',
              show_default=True)
@click.option('--limit', type=int,
              help='''The number of Subscriptions's to limit in the resultset whose default value 10.''',
              show_default=True)
@click.option('--sort_by', type=str,
              help='''SortBy field name.''',
              show_default=True)
@click.option('--order', type=str,
              help='''order query parameter.''',
              show_default=True)
@click.option('--headers', type=str, help='''Dictionary of HTTP Headers to send with the Request.''',
              default=None,
              show_default=True)
@click.option('-pp', '--pretty_print', type=int, help='''Pretty print indent''',
              default=None,
              show_default=True)
@click.option('--beep', is_flag=True, help='''Spinner beep (on)''')
@click.pass_obj
def get_event_subscriptions(obj, pretty_print, beep,
                            event_ids,
                            offset,
                            limit,
                            sort_by,
                            order,
                            headers):
    """Gets the list of Subscriptions's based on provided offset and limit.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_event_subscriptions(
            event_ids=event_ids,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            order=order,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)


@event_management.command()
@click.option('--execution_id', type=str,
              help='''Execution ID.''',
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
def get_status_api_for_events(obj, pretty_print, beep,
                              execution_id,
                              headers):
    """Get the Status of events API calls with provided executionId as mandatory path parameter.
    """
    spinner = init_spinner(beep=beep)
    start_spinner(spinner)
    try:
        if headers is not None:
            headers = json.loads(headers)
        result = obj.get_status_api_for_events(
            execution_id=execution_id,
            headers=headers)
        stop_spinner(spinner)
        opprint(result, indent=pretty_print)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('Error:', e)
        click.Context.exit(-1)
