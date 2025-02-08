from models import db
from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    games = db.relationship('Game', secondary='loans', back_populates='customers')
    loans = db.relationship('Loan', back_populates='customer')
