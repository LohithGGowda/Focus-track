from flask import Blueprint, request, jsonify
from models import db,card,entries


basercheck = Blueprint('basercheck', __name__)
@basercheck.route('/')

def bcheck():
    return jsonify({"message": "up and running base page"}), 201

card_routes = Blueprint('card_routes',__name__)
@card_routes.route('/add_card', methods = ['POST'])

def add_card():
    card_name = request.json.get('name')
    if not card_name:
        return jsonify({"error": "Card name is required"}),400
    
    existing_card = card.query.filter_by(card_name=card_name).first()
    if existing_card :
        return jsonify({"error" : "Card already exists","card_id" : existing_card.card_id}), 200

    new_card = card(card_name=card_name)
    db.session.add(new_card)
    db.session.commit()
    

    return jsonify({"message": "sucessfully added the new card", "card_id":new_card.card_id}), 201

# @card_routes.route('/test_request', methods=['POST'])
# def test_request():
#     print("Raw request data:", request.get_json())  # See ALL incoming data
#     print("Headers:", dict(request.headers))
#     return jsonify({"received": request.get_json()}), 200


# adding ENTRIES to entries table used for analysis and storage

@card_routes.route('/add_entry',methods= ['POST']) 


# Restful post : recieve
def entry():    
    data = request.json
    card_id = data.get('card_id')
    input_text = data.get('input_text','')  # optional txt added by user

# Restful post : validate

    #CHECK FOR NON EMPTY ENTRY
    if not card_id:
        return jsonify({"error" : "u must choose a card"}), 400  # client error

    # verify if card exists
    selected_card = card.query.get(card_id)
    if not selected_card:
        return jsonify({"error" : 'card not found'}), 404 # invalid request 
    
# Restful post : process

    # create new entry
    new_entry = entries(card_id=card_id,input_text=input_text)
    db.session.add(new_entry)
    db.session.commit()

# Restful post : Respond
    return jsonify({
        "message": f"good to know u completed a task sucessfully by doing {input_text}",
        "entry_id": new_entry.id,
        "card_name": selected_card.card_name,
        "input_text": input_text
    }), 201 # sucessful post request


# To fetch db cards to frontend
@card_routes.route('/cards',methods= ['GET'])
def list_cards() : 
    cards_list = card.query.all()
    
    return jsonify([{
        "card_id" : c.card_id,
        "card_name" : c.card_name
    }for c in cards_list]),200

