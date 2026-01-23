from flask import Flask
from models import db
from routecards import card_routes # projects routes file or blueprint
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./selections.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'selections.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 

app.register_blueprint(card_routes) # Register routes blueprint

with app.app_context():
    db.create_all()
    print("Database tables created (or already exist) within the app context.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # ok for local dev
