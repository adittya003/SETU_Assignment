class MerchantNotFoundException(Exception):
    """
    Raised when the merchant does not exist.
    """

    def __init__(self, merchant_id):
        super().__init__(
            f"Merchant with ID '{merchant_id}' does not exist."
        )