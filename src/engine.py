import time
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MerchantConfig:
    merchant_id: str
    threshold: float  # fraud score threshold

@dataclass
class Transaction:
    transaction_id: str
    merchant_id: str
    amount: float
    card_number: str
    timestamp: float  # epoch seconds

@dataclass
class TransactionResult:
    transaction_id: str
    fraud_score: float
    status: str  # 'approved', 'flagged', 'manual_review'

class FraudEngine:
    """ Simple fraud scoring engine. """
    def __init__(self, merchant_configs: Dict[str, MerchantConfig]):
        """ merchant_configs: mapping merchant_id -> MerchantConfig """
        self.merchant_configs = merchant_configs

    def _score(self, txn: Transaction) -> float:
        """ Compute a deterministic fraud score based on transaction data. For demo purposes: sum of digits of amount * length of card number. """
        amount_digits = sum(int(d) for d in str(txn.amount).replace(".", ""))
        card_len = len(txn.card_number)
        return amount_digits * card_len

    def process(self, txn: Transaction) -> TransactionResult:
        """ Process a transaction and return a TransactionResult. Must complete within 100 ms. """
        start = time.perf_counter()
        score = self._score(txn)
        merchant_cfg = self.merchant_configs.get(txn.merchant_id)
        if not merchant_cfg:
            raise ValueError(f"Unknown merchant {txn.merchant_id}")
        
        status = "flagged" if score > merchant_cfg.threshold else "approved"
        elapsed_ms = (time.perf_counter() - start) * 1000
        if elapsed_ms > 100:
            raise RuntimeError(f"Processing exceeded 100 ms: {elapsed_ms:.2f} ms")
        return TransactionResult(
            transaction_id=txn.transaction_id,
            fraud_score=score,
            status=status,
        )
