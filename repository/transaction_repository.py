from extension import db
from models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def find_by_transaction_id(transaction_id):
        return Transaction.query.filter_by(
            transaction_id=transaction_id
        ).first()

    @staticmethod
    def create(transaction):
        db.session.add(transaction)
        return transaction