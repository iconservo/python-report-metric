import logging

import reporter
import settings

logging.basicConfig(level=logging.DEBUG)

def setup_reporter(destination):
    # TODO, allow one off destinations
    if reporter.LIBRATO and settings.get('METRICS_LIBRATO_USER'):
        return reporter.LibratoReport(username=settings.get('METRICS_LIBRATO_USER'),
                                      api_key=settings.get('METRICS_LIBRATO_TOKEN'),
                                      source=settings.get('METRICS_LIBRATO_SOURCE', None))
    raise reporter.StatsReportException('No available destination') # maybe not right exception

def gauge(name, number, destination=None):
    '''
    Helper method for single call sending of a gauge
    :param name: metric name
    :param number: metric number
    :return: 
    '''
    try:
        setup_reporter(destination).gauge(name, number)
    except reporter.StatsReportException as e:
        #   Swallow metric related errors after logging to avoid interfering with app
        logging.exception(str(e))

def counter(name, number, destination=None):
    try:
        setup_reporter(destination).counter(name, number)
    except reporter.StatsReportException as e:
        #   Swallow metric related errors after logging to avoid interfering with app
        logging.exception(str(e))
