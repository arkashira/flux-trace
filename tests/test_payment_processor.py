import pytest
from unittest.mock import patch
from payment_processor import PaymentProcessor, Payment, PaymentStatus

@pytest.fixture
def payment_processor():
    return PaymentProcessor()

def test_process_payment_success(payment_processor):
    payment_id = 1
    payment_processor.payments[payment_id] = Payment(payment_id, PaymentStatus.SUCCESS, 0)
    payment = payment_processor.process_payment(payment_id)
    assert payment.status == PaymentStatus.SUCCESS

def test_process_payment_retry(payment_processor):
    payment_id = 1
    payment = payment_processor.process_payment(payment_id)
    assert payment.retry_count == 3
    assert payment.status == PaymentStatus.FAILED

def test_process_payment_retry_timeouts(payment_processor):
    with patch('time.sleep') as mock_sleep:
        payment_id = 1
        payment = payment_processor.process_payment(payment_id)
        assert payment.retry_count == 3
        assert payment.status == PaymentStatus.FAILED
        assert mock_sleep.call_count == 3

def test_emit_event(payment_processor):
    payment_id = 1
    payment = Payment(payment_id, PaymentStatus.FAILED, 3)
    payment_processor.emit_event(payment)
    # No assertion, just checking that the event is emitted
