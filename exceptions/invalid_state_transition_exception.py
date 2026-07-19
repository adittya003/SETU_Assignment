class InvalidStateTransitionException(Exception):
    """
    Raised when an invalid transaction state transition occurs.
    """

    def __init__(self, current_status, incoming_status):
        super().__init__(
            f"Invalid transition from "
            f"'{current_status}' to '{incoming_status}'."
        )