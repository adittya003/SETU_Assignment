class InvalidPayloadException(Exception):
    """
    Raised when the incoming payload is invalid.
    """

    def __init__(self, message):
        super().__init__(message)