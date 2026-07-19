from extension import db
from models.merchant import Merchant


class MerchantRepository:

    @staticmethod
    def find_by_merchant_id(merchant_id):
        return Merchant.query.filter_by(
            merchant_id=merchant_id
        ).first()

    @staticmethod
    def create(merchant):
        db.session.add(merchant)
        return merchant