from flask import Flask
from config import Config
from extension import db
from models.merchant import Merchant
from models.transaction import Transaction
from models.payment_event import PaymentEvent

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)


@app.route("/")
def home():
    return {"message": "Setu Assignment API"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
