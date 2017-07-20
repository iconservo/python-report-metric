
import os
import unittest
import report_metric
from report_metric import metric, reporter

# TODO break these tests across more files, logical organization TBD

def test_main():
    assert report_metric  # use your library here

def test_setup_reporter_defaults():
    # Librato is our default without config for the moment
    set_librato_credentials()
    assert isinstance(metric.setup_reporter(), reporter.LibratoReport)

def test_setup_reporter_from_parameter():
    set_librato_credentials()

    rep = metric.setup_reporter('librato')
    assert isinstance(rep, reporter.LibratoReport)

    rep = metric.setup_reporter('collectd')
    assert isinstance(rep, reporter.CollectdReport)


# TODO, these are barely smoke tests right now, making sure at least you can make the call

@unittest.skip("Breaks on credentials at the moment")
def test_librato_gauge():
    set_librato_credentials()
    rep = metric.setup_reporter('librato')
    rep.gauge("Test.SubmissionLibratoCheck", 1)

def test_collectd_gauge_submission():
    rep = metric.setup_reporter('collectd')
    rep.gauge("Test.SubmissionCollectdCheck", 1)

def test_direct_gauge_submission():
    rep = metric.setup_reporter('direct')
    rep.gauge("Test.SubmissionDirectCheck", 1)

'''
Helper Methods
'''
def set_librato_credentials():
    os.environ["METRICS_LIBRATO_USER"]="test@example.com"
    os.environ["METRICS_LIBRATO_TOKEN"]="123"
