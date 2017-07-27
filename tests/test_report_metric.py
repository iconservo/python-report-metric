
import pytest
from mock import patch, MagicMock
import report_metric
from report_metric import metric, reporter
import os

# TODO break these tests across more files, logical organization TBD
def test_main():
    assert report_metric  # use your library here

def test_setup_reporter_defaults(set_librato_credentials):
    # Librato is our default without config for the moment
    assert isinstance(metric.setup_reporter(), reporter.LibratoReport)

def test_setup_reporter_from_parameter(set_librato_credentials):
    rep = metric.setup_reporter('librato')
    assert isinstance(rep, reporter.LibratoReport)

    rep = metric.setup_reporter('collectd')
    assert isinstance(rep, reporter.CollectdReport)


# TODO, source shouldn't be unique to librato
def test_set_source_from_parameter(set_librato_credentials):
    rep = metric.setup_reporter('librato', 'custom_source')
    assert rep.source == 'custom_source'


def test_set_source_from_env_setting():
    os.environ['METRICS_SOURCE'] = 'environ_source' # probably should cleanup, but...
    rep = metric.setup_reporter('librato')
    assert rep.source == 'environ_source'


# Smoke tests to make sure "frontend" side of module is handing off to backend
@patch("report_metric.metric.setup_reporter")
def test_gauge(mock_setup_reporter):
    mock_reporter = MagicMock(spec=reporter.ReportBase)
    mock_setup_reporter.return_value = mock_reporter

    # Try
    metric.gauge("mocked-gauge", 22)

    # Verify
    mock_reporter.gauge.assert_called_once_with("mocked-gauge", 22)


# Smoke tests to make sure "frontend" side of module is handing off to backend
@patch("report_metric.metric.setup_reporter")
def test_counter(mock_setup_reporter):
    mock_reporter = MagicMock(spec=reporter.ReportBase)
    mock_setup_reporter.return_value = mock_reporter

    # Try
    metric.counter("mocked-counter")

    # Verify
    mock_reporter.counter.assert_called_once_with("mocked-counter", 1) # we expect one unless other is passed

@patch("report_metric.metric.setup_reporter")
def test_specific_source(mock_setup_reporter):
    mock_reporter = MagicMock(spec=reporter.ReportBase)
    mock_setup_reporter.return_value = mock_reporter

    metric.gauge("mocked-gauge", 123, source="one-off-source")

    mock_reporter.gauge.assert_called_once_with("mocked-gauge", 123) # we expect one unless other is passed
    mock_setup_reporter.assert_called_once_with(None, "one-off-source") # as as setup_reporter is sent the parameter, other test make sure it's used


# TODO better tests, these are barely smoke tests
@pytest.mark.skip("Breaks on credentials at the moment")
def test_librato_gauge(set_librato_credentials):
    rep = metric.setup_reporter('librato')
    rep.gauge("Test.SubmissionLibratoCheck", 1)

def test_collectd_gauge_submission():
    rep = metric.setup_reporter('collectd')
    rep.gauge("Test.SubmissionCollectdCheck", 1)

def test_direct_gauge_submission():
    rep = metric.setup_reporter('direct')
    rep.gauge("Test.SubmissionDirectCheck", 1)
