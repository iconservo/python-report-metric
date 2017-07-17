
import os
import report_metric
from report_metric import metric, reporter

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

def set_librato_credentials():
    os.environ["METRICS_LIBRATO_USER"]="test@example.com"
    os.environ["METRICS_LIBRATO_TOKEN"]="123"
