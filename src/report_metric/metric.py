import logging

import reporter
import settings

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
    try:
        setup_reporter(destination).gauge(name, number)
    except reporter.StatsReportException as e:
        #   Swallow metric related errors after logging to avoid interfering with app
        logging.exception(str(e))
