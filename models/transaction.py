from enums.reconciliation_status import ReconciliationStatus
from extension import db
from sqlalchemy import Enum ,UUID
from enums.transaction_status import TransactionStatus
import uuid

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    merchant_id = db.Column(
        db.Integer,
        db.ForeignKey("merchants.id"),
        nullable=False,
        index=True
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    currency = db.Column(
        db.String(10),
        nullable=False
    )

    status = db.Column(
        Enum(TransactionStatus),
        nullable=False
    )

    reconciliation_status = db.Column(
        Enum(ReconciliationStatus),
        nullable=False,
        default=ReconciliationStatus.PENDING
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    merchant = db.relationship(
        "Merchant",
        backref="transactions"
    )

    def __repr__(self):
        return f"<Transaction {self.transaction_id}>"