from models.transaction import Transaction
from extension import db


class TransactionService:

    @staticmethod
    def get_by_transaction_id(transaction_id):
        """
        Returns the transaction if it exists, else None.
        """
        return Transaction.query.filter_by(
            transaction_id=transaction_id
        ).first()

    @staticmethod
    def exists(transaction_id):
        """
        Returns True if the transaction exists.
        """
        return Transaction.query.filter_by(
            transaction_id=transaction_id
        ).first() is not None

    @staticmethod
    def create_transaction(
        transaction_id,
        merchant_id,
        amount,
        currency,
        status,
        reconciliation_status
    ):
        """
        Creates a new transaction.
        """
        transaction = Transaction(
            transaction_id=transaction_id,
            merchant_id=merchant_id,
            amount=amount,
            currency=currency,
            status=status,
            reconciliation_status=reconciliation_status
        )

        db.session.add(transaction)
        return transaction

    @staticmethod
    def update_status(transaction, status ,reconciliation_status):
        """
        Updates the transaction status.
        """
        transaction.status = status
        transaction.reconciliation_status = reconciliation_status