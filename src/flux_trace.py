import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class Metric:
    total_transactions: int
    average_latency: float
    error_rate: float

class FluxTrace:
    def __init__(self):
        self.metrics = Metric(0, 0.0, 0.0)
        self.transactions = []
        self.last_scrape_time = time.time()

    def add_transaction(self, latency: float, success: bool):
        self.transactions.append((latency, success))
        self.metrics.total_transactions += 1
        self.metrics.average_latency = sum(latency for latency, _ in self.transactions) / len(self.transactions)
        self.metrics.error_rate = sum(1 for _, success in self.transactions if not success) / len(self.transactions)

    def scrape_metrics(self) -> Dict[str, float]:
        if time.time() - self.last_scrape_time < 15:
            return {}
        self.last_scrape_time = time.time()
        return {
            'total_transactions': self.metrics.total_transactions,
            'average_latency': self.metrics.average_latency,
            'error_rate': self.metrics.error_rate
        }

    def check_alert(self) -> bool:
        if len(self.transactions) < 100:
            return False
        latency_percentile = sorted([latency for latency, _ in self.transactions])[-5]
        return latency_percentile > 1.0
