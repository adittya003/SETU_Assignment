from extension import db
from models.payment_event import PaymentEvent


class PaymentEventRepository:

    @staticmethod
    def find_by_event_id(event_id):
        return PaymentEvent.query.filter_by(
            event_id=event_id
        ).first()

    @staticmethod
    def find_by_transaction(transaction_db_id):
        return PaymentEvent.query.filter_by(
            transaction_id=transaction_db_id
        ).all()

    @staticmethod
    def create(payment_event):
        db.session.add(payment_event)
        return payment_event