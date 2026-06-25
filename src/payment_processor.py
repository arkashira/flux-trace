import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class PaymentStatus(Enum):
    PENDING = 1
    FAILED = 2
    SUCCESS = 3

@dataclass
class Payment:
    id: int
    status: PaymentStatus
    retry_count: int

class PaymentProcessor:
    def __init__(self):
        self.payments = {}

    def process_payment(self, payment_id: int) -> Optional[Payment]:
        if payment_id not in self.payments:
            self.payments[payment_id] = Payment(payment_id, PaymentStatus.PENDING, 0)
        payment = self.payments[payment_id]
        if payment.status == PaymentStatus.SUCCESS:
            return payment
        if payment.retry_count < 3:
            time.sleep([1, 5, 15][payment.retry_count])
            payment.retry_count += 1
            self.payments[payment_id] = payment
            return self.process_payment(payment_id)
        else:
            payment.status = PaymentStatus.FAILED
            self.payments[payment_id] = payment
            return payment

    def emit_event(self, payment: Payment) -> None:
        print(f"Payment {payment.id} failed")
