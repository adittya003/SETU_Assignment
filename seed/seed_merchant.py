import json

from app import app
from extension import db
from models.merchant import Merchant

MERCHANT_FILE = "seed/merchants.json"

with app.app_context():

    with open(MERCHANT_FILE, "r", encoding="utf-8") as f:
        merchants = json.load(f)

    for merchant_data in merchants:

        merchant_id = merchant_data["merchant_id"]
        merchant_name = merchant_data["merchant_name"]

        # Skip if already exists
        existing = Merchant.query.filter_by(merchant_id=merchant_id).first()

        if existing:
            print(f"{merchant_name} ({merchant_id}) already exists.")
            continue

        merchant = Merchant(
            merchant_id=merchant_id,
            merchant_name=merchant_name
        )

        db.session.add(merchant)

    db.session.commit()

print("Merchants inserted successfully.")