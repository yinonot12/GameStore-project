from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request, jsonify, session
from models import db
from models.admin import Admin
from models.Customer import Customer
from models.game import Game


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_store.db'
db.init_app(app)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'



CORS(app, 
     resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://127.0.0.1:5502"]}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

@app.after_request
def apply_cors_headers(response):
    origin = request.headers.get('Origin')
    allowed_origins = ["http://127.0.0.1:5500", "http://127.0.0.1:5502"]
    
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response.headers['Access-Control-Expose-Headers'] = '*'
        response.headers["Access-Control-Max-Age"] = "3600"
    
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Max-Age'] = '1'
    
    return response

@app.route('/')
def home():
    return "Game Store API is running!"

@app.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    data = request.json
    admin = Admin.query.filter_by(username=data['username'], password=data['password']).first()
    if admin:
        session['admin_id'] = admin.id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/logout', methods=['OPTIONS', 'POST'])
def logout():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    session.pop('admin_id', None)
    return jsonify({"message": "Logged out"}), 200


@app.route('/loans', methods=['GET'])
def view_loans():
    games = Game.query.filter_by(loan_status=True).all()
    return jsonify([{ "title": g.title, "customer": g.customer.name } for g in games])

@app.route('/customers', methods=['OPTIONS', 'POST'])
def add_customer():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer registered successfully"}), 201


@app.route('/loans', methods=['OPTIONS', 'POST', 'GET'])
def loan_game():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    if request.method == 'POST':
        data = request.json
        game = Game.query.get(data['game_id'])
        customer = Customer.query.get(data['customer_id'])
        if game and customer and not game.loan_status:
            game.loan_status = True
            game.customer_id = customer.id
            db.session.commit()
            return jsonify({"message": "Game loaned successfully"}), 200
        return jsonify({"message": "Invalid request or game already loaned"}), 400

    if request.method == 'GET':
        games = Game.query.filter_by(loan_status=True).all()
        return jsonify([{ "title": g.title, "customer": g.customer.name } for g in games])

@app.route('/games/<int:game_id>', methods=['OPTIONS', 'DELETE'])
def delete_game(game_id):
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({"message": "Game deleted"}), 200
    return jsonify({"message": "Game not found"}), 404

@app.route('/games', methods=['OPTIONS', 'GET', 'POST'])
def manage_games():
    if request.method == 'OPTIONS':
        return jsonify({"message": "OK"}), 200
    if request.method == 'GET':
        if 'admin_id' not in session:
            return jsonify({"error": "Unauthorized access"}), 403
        games = Game.query.all()
        return jsonify([{ "id": g.id, "title": g.title, "genre": g.genre, "price": g.price, "quantity": g.quantity, "loan_status": g.loan_status } for g in games])
    
    if request.method == 'POST':
        data = request.json
        new_game = Game(title=data['title'], genre=data['genre'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_game)
        db.session.commit()
        return jsonify({"message": "Game added successfully"}), 201




if __name__ == "__main__":
   app.run(debug=True, port=5501)
   with app.app_context():
     db.create_all()
     print("Database tables created successfully!")
     print(Admin.query.all())

