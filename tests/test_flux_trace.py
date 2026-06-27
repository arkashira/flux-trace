from flux_trace import FluxTrace, Metric
import pytest
import time

def test_add_transaction():
    flux_trace = FluxTrace()
    flux_trace.add_transaction(0.5, True)
    assert flux_trace.metrics.total_transactions == 1
    assert flux_trace.metrics.average_latency == 0.5
    assert flux_trace.metrics.error_rate == 0.0

def test_add_multiple_transactions():
    flux_trace = FluxTrace()
    flux_trace.add_transaction(0.5, True)
    flux_trace.add_transaction(1.0, False)
    assert flux_trace.metrics.total_transactions == 2
    assert flux_trace.metrics.average_latency == 0.75
    assert flux_trace.metrics.error_rate == 0.5

def test_scrape_metrics():
    flux_trace = FluxTrace()
    flux_trace.add_transaction(0.5, True)
    flux_trace.last_scrape_time = time.time() - 16  # Ensure scrape is allowed
    metrics = flux_trace.scrape_metrics()
    assert metrics['total_transactions'] == 1
    assert metrics['average_latency'] == 0.5
    assert metrics['error_rate'] == 0.0

def test_scrape_metrics_too_soon():
    flux_trace = FluxTrace()
    flux_trace.add_transaction(0.5, True)
    flux_trace.last_scrape_time = time.time()
    metrics = flux_trace.scrape_metrics()
    assert metrics == {}

def test_check_alert():
    flux_trace = FluxTrace()
    for _ in range(100):
        flux_trace.add_transaction(1.1, True)
    assert flux_trace.check_alert()

def test_check_alert_not_enough_data():
    flux_trace = FluxTrace()
    for _ in range(50):
        flux_trace.add_transaction(1.1, True)
    assert not flux_trace.check_alert()
