from flask import Blueprint, request, jsonify
from models import db
from app import app

card_routes = Blueprint('card_routes',__name__)

@card_routes.route('/add_card', methods = ['POST'])

def add_card():
    card_name = request.json.get('name')
    if not card_name:
        return jsonify({"error": "Card name is required"}),400
    
    existing_card = card.query.filter_by(name=card_name).first()
    if existing_card :
        return jsonify({"error" : "Card already exists","card_id" : existing_card.id}), 200

    new_card = card(name=card_name)
    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message": "sucessfully added the new card", "card_id":new_card.id}), 201