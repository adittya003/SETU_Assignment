from sqlalchemy import UUID,Enum
from enums.event_type import EventType

from extension import db

class PaymentEvent(db.Model):
    __tablename__ = "payment_events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    event_id = db.Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id"),
        nullable=False,
        index=True
    )

    event_type = db.Column(
        Enum(EventType),
        nullable=False
    )

    event_timestamp = db.Column(
        db.DateTime,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    transaction = db.relationship(
        "Transaction",
        backref="events"
    )

    def __repr__(self):
        return f"<PaymentEvent {self.event_id}>"