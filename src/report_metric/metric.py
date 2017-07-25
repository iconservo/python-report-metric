import logging

import reporter
import settings
from celery.task import task

logging.basicConfig(level=logging.DEBUG)

def setup_reporter(destination = None):
    destination = destination or settings.get('METRICS_DESTINATION', 'librato')
    if destination == 'librato' and reporter.LIBRATO and settings.get('METRICS_LIBRATO_USER'):
        return reporter.LibratoReport(username=settings.get('METRICS_LIBRATO_USER'),
                                      api_key=settings.get('METRICS_LIBRATO_TOKEN'),
                                      source=settings.get('METRICS_LIBRATO_SOURCE', None))

    elif destination == 'collectd' and reporter.COLLECTD:
        return reporter.CollectdReport()
    elif destination == 'direct':
        return reporter.DirectReport()
    raise reporter.StatsReportException('No available/configured destination') # maybe not right exception

def gauge(name, number, destination=None):
    '''
    Helper method for single call sending of a gauge
    :param name: metric name
    :param number: metric number
    :param destination: optional, if not sending to default
    :return: 
    '''
    if settings.get('METRICS_USE_CELERY', False):
        _report_gauge.delay(name, number, destination)
    else:
        _report_gauge(name, number, destination)

def counter(name, number=1, destination=None):
    '''
    Helper method for single call sending of a counter
    :param name: metric name
    :param number: metric number
    :param destination: optional, if not sending to default
    :return:
    '''
    if settings.get('METRICS_USE_CELERY', False):
        _report_counter.delay(name, number, destination)
    else:
        _report_counter(name, number, destination)


# There's got to be a more elegant way to conditionally wrap a function in Task, but for the moment
@task(name='report_metric.gauge')
def _report_gauge(name, number, destination=None):
    try:
        setup_reporter(destination).gauge(name, number)
    except reporter.StatsReportException as e:
        logging.exception(str(e))

@task(name='report_metric.counter')
def _report_counter(name, number=1, destination=None):
    try:
        setup_reporter(destination).counter(name, number)
    except reporter.StatsReportException as e:
        logging.exception(str(e))
