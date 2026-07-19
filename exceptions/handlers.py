from flask import jsonify

from exceptions import (
    DuplicateEventException,
    InvalidPayloadException,
    MerchantNotFoundException
)


def register_error_handlers(app):

    @app.errorhandler(InvalidPayloadException)
    def handle_invalid_payload(error):
        return jsonify({
            "error": str(error)
        }), 400


    @app.errorhandler(MerchantNotFoundException)
    def handle_merchant_not_found(error):
        return jsonify({
            "error": str(error)
        }), 404


    @app.errorhandler(DuplicateEventException)
    def handle_duplicate_event(error):
        return jsonify({
            "message": str(error)
        }), 200


    @app.errorhandler(Exception)
    def handle_internal_server_error(error):
        raise error