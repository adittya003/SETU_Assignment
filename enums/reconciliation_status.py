from enum import Enum


class ReconciliationStatus(Enum):
    MATCHED = "MATCHED"
    PENDING = "PENDING"
    DISCREPANCY = "DISCREPANCY"