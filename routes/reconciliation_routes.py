from flask import Blueprint, jsonify

from services.reconciliation_service import ReconciliationService

reconciliation_bp = Blueprint("reconciliation", __name__)


@reconciliation_bp.route("/reconciliation/summary", methods=["GET"])
def get_summary():

    return jsonify(
        ReconciliationService.get_summary()
    ), 200


@reconciliation_bp.route("/reconciliation/discrepancies", methods=["GET"])
def get_discrepancies():

    return jsonify(
        ReconciliationService.get_discrepancies()
    ), 200