from . import db

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    loans = db.relationship('Loan', back_populates='game')
    customers = db.relationship('Customer', secondary='loans', back_populates='games')


