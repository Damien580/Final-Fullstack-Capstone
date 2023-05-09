import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_bio = db.Column(db.Text, nullable=True)
    user_email = db.Column(db.String, nullable=False)
    is_female = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, username, password, user_bio, user_email, is_female):
        self.username = username
        self.password = password
        self.user_bio = user_bio
        self.user_email = user_email
        self.is_female = is_female
    
    def __repr__(self):
        return f"<User: ID={self.id} Username={self.username} Email={self.user_email}>"

class Picture(db.Model):
    __tablename__ = "pictures"
    
    pic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pic_url = db.Column(db.String, nullable=False)
    comment = db.Column(db.Text)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    def __repr__(self):
        return f"<Picture: pic_id={self.pic_id}"
    

class Message(db.Model):
    __tablename__ = "messages"
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String, nullable=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])
    
    def get_time(self):
        return self.timestamp.strftime("%b %d, %Y %H:%M:%S")
    
    def __repr__(self):
        return f"<Message={self.message}>"

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to the db!")
    
if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)