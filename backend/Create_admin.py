from models import db
from models.admin import Admin
from app import app  # ודא שהאפליקציה שלך מוגדרת ב-app.py

with app.app_context():
    # מחיקת אדמינים קיימים רק לצורך הדגמה (לא חובה לשימוש בייצור)
    db.drop_all()
    db.create_all()

    # יצירת אדמין חדש
    admin = Admin(username='yinonot', password='zxzx2121')
    db.session.add(admin)
    db.session.commit()

    print("Admin user created successfully!")
