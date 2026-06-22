from payment_engine import PaymentEngine, PaymentRequest, PaymentResponse
import pytest
from datetime import datetime, timedelta

def test_submit_payment():
    payment_engine = PaymentEngine()
    payment_request = PaymentRequest(100.0, 1)
    payment_response = payment_engine.submit_payment(payment_request)
    assert payment_response.transaction_id
    assert payment_response.settlement_estimate
    assert payment_engine.get_transaction(payment_response.transaction_id) == {'status': 'pending', 'amount': 100.0}

def test_get_transaction():
    payment_engine = PaymentEngine()
    payment_request = PaymentRequest(100.0, 1)
    payment_response = payment_engine.submit_payment(payment_request)
    transaction = payment_engine.get_transaction(payment_response.transaction_id)
    assert transaction == {'status': 'pending', 'amount': 100.0}

def test_settlement_estimate_accuracy():
    payment_engine = PaymentEngine()
    payment_request = PaymentRequest(100.0, 1)
    payment_response = payment_engine.submit_payment(payment_request)
    settlement_estimate = datetime.strptime(payment_response.settlement_estimate, '%Y-%m-%d')
    actual_settlement_time = datetime.now() + timedelta(days=3)
    assert abs((settlement_estimate - actual_settlement_time).days) <= 5

def test_submit_payment_edge_case_zero_amount():
    payment_engine = PaymentEngine()
    payment_request = PaymentRequest(0.0, 1)
    with pytest.raises(ValueError):
        payment_engine.submit_payment(payment_request)

def test_submit_payment_edge_case_negative_amount():
    payment_engine = PaymentEngine()
    payment_request = PaymentRequest(-100.0, 1)
    with pytest.raises(ValueError):
        payment_engine.submit_payment(payment_request)
