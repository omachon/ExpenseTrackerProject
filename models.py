from datetime import datetime
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    expenses = db.relationship('Category', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expenses = db.relationship('Expense', backref='category', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def add_sample_data():
    user = User(username='testuser')
    db.session.add(user)
    db.session.commit()

    expense_data = [
        {'amount': 100.0, 'category': 'Food', 'description': 'Groceries', 'date': datetime(2023, 1, 10), 'user_id': user.id},
        {'amount': 50.0, 'category': 'Transport', 'description': 'Bus pass', 'date': datetime(2023, 1, 11), 'user_id': user.id},
        {'amount': 200.0, 'category': 'Bills', 'description': 'Electricity', 'date': datetime(2023, 1, 15), 'user_id': user.id},
        {'amount': 80.0, 'category': 'Entertainment', 'description': 'Movies', 'date': datetime(2023, 1, 20), 'user_id': user.id},
    ]

    for expense in expense_data:
        db.session.add(Expense(**expense))
    db.session.commit()