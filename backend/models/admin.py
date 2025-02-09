from sqlalchemy import String
from . import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(String(100), nullable=False)
    password = db.Column(db.String(15),primary_key=False)
    email = db.Column(db.String(25), primary_key=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def authenticate(username, password):
        return Admin.query.filter_by(username=username, password=password).first()


