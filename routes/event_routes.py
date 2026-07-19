from flask import Blueprint, jsonify, request

from services.event_processing_service import EventProcessingService
from services.transaction_service import TransactionService

event_bp = Blueprint("events", __name__)

@event_bp.route("/events", methods=["POST"])
def process_event():
    payload = request.get_json()

    transaction = EventProcessingService.process_event(payload)

    return jsonify({
        "message": "Event processed successfully.",
        "transaction_id": str(transaction.transaction_id),
        "status": transaction.status.value,
        "reconciliation_status": transaction.reconciliation_status.value
    }), 200

#---------------------------------------------------------------------------------------------------------------
@event_bp.route("/transactions/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    transaction = TransactionService.get_by_transaction_id(transaction_id)

    if not transaction:
        return jsonify({
            "message": "Transaction not found."
        }), 404

    return jsonify({
        "transaction_id": str(transaction.transaction_id),
        "merchant_id": transaction.merchant.merchant_id,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "status": transaction.status.value,
        "reconciliation_status": transaction.reconciliation_status.value
    }), 200

#---------------------------------------------------------------------------------------------------------------
@event_bp.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = TransactionService.get_all()

    return jsonify([
        {
            "transaction_id": str(transaction.transaction_id),
            "merchant_id": transaction.merchant.merchant_id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "status": transaction.status.value,
            "reconciliation_status": transaction.reconciliation_status.value
        }
        for transaction in transactions
    ]), 200