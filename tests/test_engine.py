import pytest
from src.engine import FraudEngine, MerchantConfig, Transaction, TransactionResult

def test_process_transaction():
    merchant_configs = {
        "m1": MerchantConfig(merchant_id="m1", threshold=100),
    }
    engine = FraudEngine(merchant_configs)
    txn = Transaction(
        transaction_id="t1",
        merchant_id="m1",
        amount=10.99,
        card_number="1234567890123456",
        timestamp=1643723400,
    )
    result = engine.process(txn)
    assert result.transaction_id == "t1"
    assert result.status in ["approved", "flagged"]

def test_unknown_merchant():
    merchant_configs = {
        "m1": MerchantConfig(merchant_id="m1", threshold=100),
    }
    engine = FraudEngine(merchant_configs)
    txn = Transaction(
        transaction_id="t2",
        merchant_id="m2",
        amount=10.99,
        card_number="1234567890123456",
        timestamp=1643723400,
    )
    with pytest.raises(ValueError):
        engine.process(txn)

def test_processing_time():
    merchant_configs = {
        "m1": MerchantConfig(merchant_id="m1", threshold=100),
    }
    engine = FraudEngine(merchant_configs)
    txn = Transaction(
        transaction_id="t1",
        merchant_id="m1",
        amount=10.99,
        card_number="1234567890123456",
        timestamp=1643723400,
    )
    result = engine.process(txn)
    assert result.transaction_id == "t1"
    assert result.status in ["approved", "flagged"]
