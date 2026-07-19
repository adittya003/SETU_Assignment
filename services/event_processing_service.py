from uuid import UUID
from datetime import datetime

from exceptions import (
    DuplicateEventException,
    InvalidPayloadException,
    MerchantNotFoundException
)


from enums.reconciliation_status import ReconciliationStatus
from extension import db
from enums.event_type import EventType
from enums.transaction_status import TransactionStatus

from services.merchant_service import MerchantService
from services.transaction_service import TransactionService
from services.payment_event_service import PaymentEventService


class EventProcessingService:

    @staticmethod
    def process_event(payload):
        """
        Orchestrates the complete payment event processing workflow.
        """
        try:

            # 1. Validate payload
            EventProcessingService.validate_payload(payload)

            # 2. Check idempotency
            transaction_id = payload["transaction_id"]
            merchant_id = payload["merchant_id"]
            transaction = TransactionService.get_by_transaction_id(transaction_id)

            if PaymentEventService.exists(payload["event_id"]):
                raise DuplicateEventException(payload["event_id"])
            

            # 3. Ensure merchant exists
            merchant = MerchantService.get_by_id(merchant_id)
            if not merchant:
                raise MerchantNotFoundException(merchant_id)
            
            if merchant.merchant_name != payload["merchant_name"]:
                raise InvalidPayloadException("merchant_name does not match the provided merchant_id.")
            

            event_type = payload["event_type"]
            payload_status = EventProcessingService.map_event_to_transaction_status(event_type)

            # 4. Check if transaction exists
            if transaction:
                db_status = transaction.status

                # Valid transitions
                if (
                    db_status == TransactionStatus.INITIATED
                    and payload_status == TransactionStatus.PROCESSED
                ):
                    TransactionService.update_status(
                        transaction,
                        payload_status,
                        ReconciliationStatus.PENDING
                    )

                elif (
                    db_status == TransactionStatus.PROCESSED
                    and payload_status == TransactionStatus.SETTLED
                ):
                    TransactionService.update_status(
                        transaction,
                        payload_status,
                        ReconciliationStatus.MATCHED
                    )

                # Every other transition is a discrepancy
                else:
                    TransactionService.update_status(
                        transaction,
                        payload_status,
                        ReconciliationStatus.DISCREPANCY
                    )
                
                
                
            else:
                # 5. Create new transaction
                if payload_status == TransactionStatus.INITIATED:
                    transaction = TransactionService.create_transaction(
                        transaction_id=transaction_id,
                        merchant_id=merchant.id,
                        amount=payload["amount"],
                        currency=payload["currency"],
                        status=payload_status,
                        reconciliation_status=ReconciliationStatus.PENDING
                    )
                else:
                    # If the first event is not INITIATED, it's a discrepancy
                    transaction = TransactionService.create_transaction(
                        transaction_id=transaction_id,
                        merchant_id=merchant.id,
                        amount=payload["amount"],
                        currency=payload["currency"],
                        status=payload_status,
                        reconciliation_status=ReconciliationStatus.DISCREPANCY
                    )
            db.session.flush()

            # 6. Log the event
            PaymentEventService.create_event(
                event_id = payload["event_id"],
                transaction_id = transaction.id,
                event_type = EventType(payload["event_type"]),
                event_timestamp = datetime.fromisoformat(payload["timestamp"])
            )

            # 7. Commit all changes
            db.session.commit()

            # 8. Return the updated or newly created transaction
            return transaction
        
        except Exception:
            db.session.rollback()
            raise



# ----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def validate_payload(payload):
        """
        Validates the incoming event payload.
        Raises ValueError if validation fails.
        """

        required_fields = [
            "event_id",
            "event_type",
            "transaction_id",
            "merchant_id",
            "merchant_name",
            "amount",
            "currency",
            "timestamp"
        ]

        # Check required fields
        for field in required_fields:
            if field not in payload:
                raise InvalidPayloadException(f"Missing required field: {field}")

        # Validate UUIDs
        try:
            UUID(payload["event_id"])
        except ValueError:
            raise InvalidPayloadException("Invalid event_id.")

        try:
            UUID(payload["transaction_id"])
        except ValueError:
            raise InvalidPayloadException("Invalid transaction_id.")

        # Validate event type
        try:
            EventType(payload["event_type"])
        except ValueError:
            raise InvalidPayloadException(f"Invalid event type: {payload['event_type']}")

        # Validate amount
        if not isinstance(payload["amount"], (int, float)):
            raise InvalidPayloadException("Amount must be numeric.")

        if payload["amount"] <= 0:
            raise InvalidPayloadException("Amount must be greater than zero.")

        # Validate merchant_id
        if not isinstance(payload["merchant_id"], str) or not payload["merchant_id"].strip():
            raise InvalidPayloadException("Invalid merchant_id.")

        # Validate merchant_name
        if not isinstance(payload["merchant_name"], str) or not payload["merchant_name"].strip():
            raise InvalidPayloadException("Invalid merchant_name.")

        # Validate currency
        if not isinstance(payload["currency"], str) or not payload["currency"].strip():
            raise InvalidPayloadException("Invalid currency.")

        # Validate timestamp
        try:
            datetime.fromisoformat(payload["timestamp"])
        except ValueError:
            raise InvalidPayloadException("Invalid timestamp.")
    

#----------------------------------------------------------------------------------------------------------------------


    @staticmethod
    def map_event_to_transaction_status(event_type):
        """
        Maps an event type to its corresponding transaction status.
        """

        event_type = EventType(event_type)

        mapping = {
            EventType.INITIATED: TransactionStatus.INITIATED,
            EventType.PROCESSED: TransactionStatus.PROCESSED,
            EventType.FAILED: TransactionStatus.FAILED,
            EventType.SETTLED: TransactionStatus.SETTLED,
        }

        return mapping[event_type]