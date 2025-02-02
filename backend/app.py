
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from models.admin import Admin
from models.Customer import Customer
from models.game import Game
from models.loan import Loan

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_store.db'
db.init_app(app)

@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added to inventory.'}), 201

@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()
        games_list = [
            {
                'id': game.id,
                'title': game.title,
                'genre': game.genre,
                'price': game.price,
                'quantity': game.quantity
            } for game in games
        ]
        return jsonify({
            'message': 'Games retrieved successfully',
            'games': games_list
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer registered successfully.'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_list = [
        {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone
        } for customer in customers
    ]
    return jsonify({
        'message': 'Customers retrieved successfully',
        'customers': customers_list
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
