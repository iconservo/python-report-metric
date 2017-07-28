"""The purpose of this module is to unify the API for metrics collection services
"""
import re

try:
    import collectd
    collectd.SEND_INTERVAL = 0.5
    collectd.start_threads()

    COLLECTD = True
except ImportError:  # pragma: nocover
    COLLECTD = False
try:
    import librato
    import socket

    LIBRATO = True
except ImportError:  # pragma: nocover
    LIBRATO = False
try:
    import newrelic.agent

    NEWRELIC = True
except ImportError:  # pragma: nocover
    NEWRELIC = False

import backends.direct

class StatsReportException(Exception):
    pass

class ReportBase(object):
    """Report metrics by name/value.
    Name is required to be given in dotted notation, with foo.bar.b
    First part of the name is treated as prefix, depending on metrics backend
    """

    def __init__(self):
        self.pattern = re.compile(ur'^(?:([A-Za-z]+)\.([A-Za-z0-9-\.\_]+))$')

    def gauge(self, name, number):
        """Report absolute gauge value
        """
        prefix, metric = self._validate_name(name)
        if not self._gauge(prefix, metric, float(number)):
            raise StatsReportException(name, number)

    def counter(self, name, number):
        """Report incrementing/decrementing counter value
        """
        prefix, metric = self._validate_name(name)
        if not self._counter(prefix, metric, float(number)):
            raise StatsReportException(name, number)

    def _validate_name(self, name):
        # TODO figure out if there's still need for prefix/suffix
        matches = re.findall(self.pattern, name)
        if len(matches) > 0:
            return matches[0][0], matches[0][1]
        else:
            raise StatsReportException("Invalid Name: " + name)


    def _dotted(self, prefix, name):
        return '{}.{}'.format(prefix, name)

    def _gauge(self, *args, **kwargs):
        raise NotImplemented

    def _counter(self, *args, **kwargs):
        raise NotImplemented


class CollectdReport(ReportBase):
    """ Report to Collectd daemon
        http://pythonhosted.org/collectd
    """

    def __init__(self, *args, **kwargs):
        self.report = collectd.Connection(*args, **kwargs)
        super(CollectdReport, self).__init__()

    def _rename(self, prefix, name):
        return '{}-{}'.format(prefix, name.replace('.', '_'))

    def _gauge(self, prefix, name, number):
        reporter = getattr(self.report, prefix)
        dictargs = {(name.replace('.', '_')): number}
        reporter.set_exact(**dictargs)
        return True

    def _counter(self, prefix, name, number):
        reporter = getattr(self.report, prefix)
        dictargs = {self._rename(prefix, name): number}
        reporter.record(**dictargs)

class DirectReport(ReportBase):
    """ Report to collectd directly TODO: rename to include collectd
    """

    def __init__(self, *args, **kwargs):
        self.report = collectd.Connection(*args, **kwargs)
        super(DirectReport, self).__init__()

    def _rename(self, prefix, name):
        return '{}-{}'.format(prefix, name.replace('.', '_'))

    def _gauge(self, prefix, name, number):
        reporter = getattr(self.report, prefix)
        #dictargs = {(name.replace('.', '_')): number}
        #reporter.set_exact(**dictargs)
        backends.direct.send_stat(name, number, prefix=prefix)
        return True

    def _counter(self, prefix, name, number):
        reporter = getattr(self.report, prefix)
        dictargs = {self._rename(prefix, name): number}
        reporter.record(**dictargs)


class LibratoReport(ReportBase):
    """ Report to Librato over http
        http://github.com/librato/python-librato
    """

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source',None)
        self.report = librato.connect(*args, **kwargs)
        self.report.set_timeout(1) # Report quick or skip it, errors will show up as missing reports
        super(LibratoReport, self).__init__()

    def _gauge(self, prefix, name, number):
        try:
            return self.report.submit(self._dotted(prefix, name), number, source=self.source) or True
        except (ValueError, socket.error) as e:
            raise StatsReportException("Error reporting to Librato", e)

    def _counter(self, prefix, name, number):
        # Librato has no API level idea of a counter, just send a gauge
        return self._gauge(prefix, name, number)


class NewRelicReport(ReportBase):
    """ Report to New Relic over http
        http://docs.newrelic.com/docs/agents/manage-apm-agents/agent-metrics/custom-metrics
    """

    def __init__(self, *args, **kwargs):
        self.reporter = newrelic.agent
        super(NewRelicReport, self).__init__()

    def _rename(self, prefix, name):
        return 'Custom/{}/{}'.format(prefix, '/'.join(name.split('.')))

    def _gauge(self, prefix, name, number):
        """Not sure if this is APM counter or gauge equivalent"""
        self.reporter.record_custom_metric(self._rename(prefix, name), number)

    def _counter(self, prefix, name, number):
        self.reporter.record_custom_metric(self._rename(prefix, name), number)


class DummyReport(ReportBase):
    """ Do nothing with the metrics
        Useful way to disable when running unit tests in a Django app
    """
    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source', None)
        super(DummyReport, self).__init__()

    def _gauge(self, prefix, name, number):
        return self._record_metric((prefix + "." + name), number)

    def _counter(self, prefix, name, number):
        return self._record_metric((prefix + "." + name), number)

    def _record_metric(self, name, number):
        return True
