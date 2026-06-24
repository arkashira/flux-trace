import pytest
from payment_engine import PaymentEngine, Transaction
import time

def test_process_transaction():
    engine = PaymentEngine()
    transaction = Transaction(1, 10.0)
    engine.process_transaction(transaction)
    assert len(engine.transactions) == 1

def test_get_transaction_latency():
    engine = PaymentEngine()
    transaction = Transaction(1, 10.0)
    engine.process_transaction(transaction)
    latency = engine.get_transaction_latency(1)
    assert latency is not None
    assert latency > 0

def test_process_transactions():
    engine = PaymentEngine()
    transactions = [Transaction(i, 10.0) for i in range(100)]
    engine.process_transactions(transactions)
    assert len(engine.transactions) == 100

def test_get_latency_stats():
    engine = PaymentEngine()
    transactions = [Transaction(i, 10.0) for i in range(100)]
    engine.process_transactions(transactions)
    latency_stats = engine.get_latency_stats()
    assert latency_stats['99.99th_percentile'] < 5
    assert latency_stats['average'] < 5

def test_payment_engine_performance():
    engine = PaymentEngine()
    transactions = [Transaction(i, 10.0) for i in range(1000)]
    start_time = time.time()
    engine.process_transactions(transactions)
    end_time = time.time()
    assert end_time - start_time < 10
