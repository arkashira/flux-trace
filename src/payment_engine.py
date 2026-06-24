import time
from dataclasses import dataclass
from typing import List

@dataclass
class Transaction:
    id: int
    amount: float
    timestamp: float = None

class PaymentEngine:
    def __init__(self):
        self.transactions = []

    def process_transaction(self, transaction: Transaction):
        transaction.timestamp = time.time()
        self.transactions.append(transaction)

    def get_transaction_latency(self, transaction_id: int):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return time.time() - transaction.timestamp
        return None

    def process_transactions(self, transactions: List[Transaction]):
        for transaction in transactions:
            self.process_transaction(transaction)

    def get_latency_stats(self):
        latencies = []
        for transaction in self.transactions:
            latency = self.get_transaction_latency(transaction.id)
            if latency is not None:
                latencies.append(latency)
        return {
            '99.99th_percentile': sorted(latencies)[int(len(latencies) * 0.9999)] if latencies else 0,
            'average': sum(latencies) / len(latencies) if latencies else 0
        }
