import logging

from celery.task import task

from report_metric import reporter
from report_metric import settings

logging.basicConfig(level=logging.DEBUG)


def setup_reporter(destination=None, source=None):
    destination = destination or settings.get('METRICS_DESTINATION', 'librato')
    source = source or settings.get('METRICS_SOURCE', None)

    if destination == 'librato' and reporter.LIBRATO and settings.get('METRICS_LIBRATO_USER'):
        return reporter.LibratoReport(username=settings.get('METRICS_LIBRATO_USER'),
                                      api_key=settings.get('METRICS_LIBRATO_TOKEN'),
                                      source=source)

    elif destination == 'collectd' and reporter.COLLECTD:
        return reporter.CollectdReport()
    elif destination == 'direct':
        return reporter.DirectReport()
    elif destination == 'dummy':
        return reporter.DummyReport()

    raise reporter.StatsReportException('No available/configured destination')  # maybe not right exception


def gauge(name, number, **kwargs):
    '''
    Helper method for single call sending of a gauge
    :param name: metric name
    :param number: metric number
    :param destination: optional, if not sending to default
    :return:
    '''
    if settings.get('METRICS_USE_CELERY', False):
        _report_gauge.delay(name, number, **kwargs)
    else:
        _report_gauge(name, number, **kwargs)


def counter(name, number=1, **kwargs):
    '''
    Helper method for single call sending of a counter
    :param name: metric name
    :param number: metric number
    :param destination: optional, if not sending to default
    :return:
    '''
    if settings.get('METRICS_USE_CELERY', False):
        _report_counter.delay(name, number, **kwargs)
    else:
        _report_counter(name, number, **kwargs)


# There's got to be a more elegant way to conditionally wrap a function in Task, but for the moment
@task(name='report_metric.gauge')
def _report_gauge(name, number, **kwargs):
    try:
        rep = setup_reporter(kwargs.get('destination', None), kwargs.get('source', None))
        rep.gauge(name, number)
    except reporter.StatsReportException as e:
        logging.exception(str(e))


@task(name='report_metric.counter')
def _report_counter(name, number=1, **kwargs):
    try:
        setup_reporter(kwargs.get('destination', None), kwargs.get('source', None)).counter(name, number)
    except reporter.StatsReportException as e:
        logging.exception(str(e))
