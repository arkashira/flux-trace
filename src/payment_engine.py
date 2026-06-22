import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class PaymentRequest:
    amount: float
    merchant_id: int

@dataclass
class PaymentResponse:
    transaction_id: str
    settlement_estimate: str

class PaymentEngine:
    def __init__(self):
        self.transactions = {}

    def submit_payment(self, payment_request: PaymentRequest) -> PaymentResponse:
        if payment_request.amount <= 0:
            raise ValueError("Payment amount must be greater than zero")
        
        transaction_id = str(datetime.now().timestamp())
        self.transactions[transaction_id] = {'status': 'pending', 'amount': payment_request.amount}
        settlement_estimate = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        return PaymentResponse(transaction_id, settlement_estimate)

    def get_transaction(self, transaction_id: str) -> Dict:
        return self.transactions.get(transaction_id, {})

def create_payment_engine() -> PaymentEngine:
    return PaymentEngine()
