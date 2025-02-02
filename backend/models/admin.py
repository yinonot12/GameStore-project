from models import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.string(25), primary_key=False)
    password = db.Column(db.string(15),primary_key=False)
    email = db.Column(db.string(25), primary_key=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def authenticate(username, password):
        return Admin.query.filter_by(username=username, password=password).first()


