from extension import db

class Merchant(db.Model):
    __tablename__ = "merchants"

    id = db.Column(db.Integer, primary_key=True)

    merchant_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    merchant_name = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Merchant {self.merchant_id} - {self.merchant_name}>"
    
