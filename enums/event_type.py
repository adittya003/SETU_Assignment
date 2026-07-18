from enum import Enum

class EventType(Enum):
    INITIATED = "payment_initiated"
    PROCESSED = "payment_processed"
    FAILED = "payment_failed"
    SETTLED = "settled"