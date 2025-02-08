from datetime import datetime
from models import db
from models.Customer import Customer

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    # קשר עם Customer
    customer = db.relationship('Customer', back_populates='loans')

    # קשר עם Game
    game = db.relationship('Game', back_populates='loans')
