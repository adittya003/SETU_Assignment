from models.merchant import Merchant


class MerchantService:

    @staticmethod
    def get_by_id(merchant_id):
        """
        Returns the merchant if it exists, else None.
        """
        return Merchant.query.filter_by(merchant_id=merchant_id).first()

    @staticmethod
    def get_by_name(merchant_name):
        """
        Returns the merchant if it exists, else None.
        """
        return Merchant.query.filter_by(merchant_name=merchant_name).first()

    @staticmethod
    def exists(merchant_id):
        """
        Returns True if the merchant exists.
        """
        return Merchant.query.filter_by(merchant_id=merchant_id).first() is not None
    