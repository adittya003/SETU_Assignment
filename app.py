from flask import Flask
from config import Config
from extension import db
from models.merchant import Merchant
from models.transaction import Transaction
from models.payment_event import PaymentEvent
from routes.event_routes import event_bp
from routes.reconciliation_routes import reconciliation_bp
from exceptions.handlers import register_error_handlers

app = Flask(__name__)

app.config.from_object(Config)


db.init_app(app)

app.register_blueprint(event_bp)
app.register_blueprint(reconciliation_bp)

register_error_handlers(app)

@app.route("/")
def home():
    return {"message": "Setu Assignment API"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
