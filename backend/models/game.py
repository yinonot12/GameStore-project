from models import db


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, title, genre, price, quantity):
        self.title = title
        self.genre = genre
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity
        }

    def __repr__(self):
        return f'<Game {self.title}>'


