from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() # Create SQLAlchemy instance


class card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    card_name = db.Column(db.String(20), unique=True, nullable=False)


class entries(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.card_id'), nullable=False)  # ✅ Foreign key to card
    input_text = db.Column (db.String(25),nullable=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    card = db.relationship('card', backref='entries') # link back to card for easy queries

print(entries.__table__.columns.keys())
print(card.__table__.columns.keys())

