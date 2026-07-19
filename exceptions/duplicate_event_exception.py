class DuplicateEventException(Exception):
    """
    Raised when an event with the same event_id
    has already been processed.
    """

    def __init__(self, event_id):
        super().__init__(
            f"Event '{event_id}' has already been processed."
        )