from enum import Enum


class TransactionStatus(Enum):
    INITIATED = "INITIATED"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"
    SETTLED = "SETTLED"