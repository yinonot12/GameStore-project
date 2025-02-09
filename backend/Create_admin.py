from models.admin import Admin
from app import app

with app.app_context():
    admin = Admin.query.filter_by(username='yinon').first()
    if admin:
        print("Admin found:", admin.username)
    else:
        print("Admin not found.")
