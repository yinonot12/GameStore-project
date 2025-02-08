from datetime import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db
from models.admin import Admin
from models.Customer import Customer
from models.game import Game
from models.loan import Loan

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # החלף במפתח סודי אמיתי
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_store.db'
db.init_app(app)

# Endpoint להוספת משחק
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

# Endpoint להחזרת רשימת משחקים
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

# Endpoint לעריכת משחק
@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    data = request.json
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found.'}), 404

    game.title = data.get('title', game.title)
    game.genre = data.get('genre', game.genre)
    game.price = data.get('price', game.price)
    game.quantity = data.get('quantity', game.quantity)

    db.session.commit()
    return jsonify({'message': 'Game updated successfully.'}), 200

# Endpoint למחיקת משחק
@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found.'}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully.'}), 200

# Endpoint להתחברות אדמין
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.verify_password(password):  # מתודה לאימות סיסמה
        session['admin_id'] = admin.id
        return jsonify({'message': 'Admin logged in successfully.'}), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_id', None)
    return jsonify({'message': 'Admin logged out successfully.'}), 200

@app.route('/loan', methods=['POST'])
def loan_game():
    try:
        data = request.json
        customer_id = data['customer_id']
        game_id = data['game_id']
        
        customer = Customer.query.get(customer_id)
        game = Game.query.get(game_id)
        
        if not customer or not game:
            return jsonify({'error': 'Customer or game not found'}), 404
        
        loan = Loan(customer_id=customer_id, game_id=game_id)
        db.session.add(loan)
        db.session.commit()
        
        return jsonify({'message': f"Game '{game.title}' successfully loaned to customer '{customer.name}'"}), 201
    except Exception as e:
        return jsonify({
            'error': 'Failed to loan the game',
            'message': str(e)
        }), 500

@app.route('/return_game/<int:loan_id>', methods=['POST'])
def return_game(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({'error': 'Loan not found with this ID'}), 404
        
        loan.return_date = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': f"Game '{loan.game.title}' successfully returned by '{loan.customer.name}'"}), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to return the game',
            'message': str(e)
        }), 500

@app.route('/loaned_games', methods=['GET'])
def display_loaned_games():
    try:
        loans = Loan.query.filter(Loan.return_date == None).all()
        if not loans:
            return jsonify({'message': 'No games are currently loaned out'}), 404
        
        loan_list = [
            {
                'game': loan.game.title,
                'customer': loan.customer.name,
                'loan_date': loan.loan_date
            } for loan in loans
        ]
        
        return jsonify({
            'message': 'Currently loaned games',
            'loans': loan_list
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve loaned games',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
