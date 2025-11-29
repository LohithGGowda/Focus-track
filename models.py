from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() # Create SQLAlchemy instance

class selection(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)

print(selection.__table__.columns.keys())
