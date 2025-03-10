from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from models.admin import Admin
from models.game import Game

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# Import models after db initialization
from models.admin import Admin
from models.game import Game

from flask_cors import CORS

CORS(app, origins=["http://127.0.0.1:5510"], supports_credentials=True)

@app.route('/games', methods=['OPTIONS', 'GET'])
def handle_games():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5510")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

    games = Game.query.all()
    games_list = [
        {
            "id": game.id,
            "title": game.title,
            "genre": game.genre,
            "price": game.price,
            "quantity": game.quantity
        }
        for game in games
    ]
    return jsonify(games_list), 200
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        admin = Admin.query.filter_by(username=data['username'], password=data['password']).first()
        
        if admin:
            return jsonify({"message": "Login successful", "success": True}), 200
        return jsonify({"message": "Invalid credentials", "success": False}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({"message": "Login failed", "success": False}), 500

@app.route('/games/', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()
        return jsonify([{
            'id': game.id,
            'title': game.title,
            'genre': game.genre,
            'price': game.price,
            'quantity': game.quantity
        } for game in games])
    except Exception as e:
        print(f"Error getting games: {str(e)}")
        return jsonify({"error": "Failed to get games"}), 500

@app.route('/games/', methods=['POST'])
def add_game():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        
        # Validate data
        if not all(key in data for key in ['title', 'genre', 'price', 'quantity']):
            return jsonify({"error": "Missing required fields"}), 400
            
        try:
            price = float(data['price'])
            quantity = int(data['quantity'])
        except ValueError:
            return jsonify({"error": "Invalid price or quantity format"}), 400

        new_game = Game(
            title=str(data['title']).strip(),
            genre=str(data['genre']).strip(),
            price=price,
            quantity=quantity
        )
        
        db.session.add(new_game)
        db.session.commit()
        print("Game added successfully:", new_game.title)  # Debug print
        return jsonify({
            "message": "Game added successfully", 
            "success": True,
            "game": {
                "id": new_game.id,
                "title": new_game.title,
                "genre": new_game.genre,
                "price": new_game.price,
                "quantity": new_game.quantity
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding game: {str(e)}")  # Debug print
        return jsonify({"error": f"Failed to add game: {str(e)}"}), 500

@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        data = request.json
        
        game.title = data['title']
        game.genre = data['genre']
        game.price = float(data['price'])
        game.quantity = int(data['quantity'])
        
        db.session.commit()
        return jsonify({"message": "Game updated successfully", "success": True})
    except Exception as e:
        db.session.rollback()
        print(f"Error updating game: {str(e)}")
        return jsonify({"error": "Failed to update game"}), 500

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return jsonify({"message": "Game deleted successfully", "success": True})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting game: {str(e)}")
        return jsonify({"error": "Failed to delete game"}), 500

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    try:
        game = Game.query.get_or_404(game_id)
        return jsonify({
            'id': game.id,
            'title': game.title,
            'genre': game.genre,
            'price': game.price,
            'quantity': game.quantity
        }), 200
    except Exception as e:
        print(f"Error getting game: {str(e)}")
        return jsonify({"error": "Failed to get game"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")
        
        # Create default admin if not exists
        admin = Admin.query.filter_by(username='yinon').first()
        if not admin:
            default_admin = Admin(username='yinon', password='admin123')
            db.session.add(default_admin)
            db.session.commit()
            print("Default admin created successfully!")
    
    app.run(debug=True, port=5501)

