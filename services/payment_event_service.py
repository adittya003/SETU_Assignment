from models.payment_event import PaymentEvent
from extension import db


class PaymentEventService:

    @staticmethod
    def get_by_event_id(event_id):
        return PaymentEvent.query.filter_by(
            event_id=event_id
        ).first()

    @staticmethod
    def exists(event_id):
        return PaymentEvent.query.filter_by(
            event_id=event_id
        ).first() is not None

    @staticmethod
    def create_event(
        event_id,
        transaction_id,
        event_type,
        event_timestamp
    ):
        payment_event = PaymentEvent(
            event_id=event_id,
            transaction_id=transaction_id,
            event_type=event_type,
            event_timestamp=event_timestamp
        )

        db.session.add(payment_event)
        return payment_event