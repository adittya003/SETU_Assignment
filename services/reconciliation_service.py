from models.transaction import Transaction

from enums.reconciliation_status import ReconciliationStatus


class ReconciliationService:

    @staticmethod
    def get_summary():
        """
        Returns a summary of reconciliation statuses.
        """

        return {
            "matched": Transaction.query.filter_by(
                reconciliation_status=ReconciliationStatus.MATCHED
            ).count(),

            "pending": Transaction.query.filter_by(
                reconciliation_status=ReconciliationStatus.PENDING
            ).count(),

            "discrepancy": Transaction.query.filter_by(
                reconciliation_status=ReconciliationStatus.DISCREPANCY
            ).count()
        }

    @staticmethod
    def get_discrepancies():
        """
        Returns all transactions with reconciliation discrepancies.
        """

        transactions = Transaction.query.filter_by(
            reconciliation_status=ReconciliationStatus.DISCREPANCY
        ).all()

        return [
            {
                "transaction_id": str(transaction.transaction_id),
                "merchant_id": transaction.merchant.merchant_id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "status": transaction.status.value,
                "reconciliation_status": transaction.reconciliation_status.value
            }
            for transaction in transactions
        ]