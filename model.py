import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Colulmn(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_bio = db.Column(db.String, nullable=True)
    user_email = db.Column(db.String, nullable=False, )
    is_female = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    def __repr__(self):
        return f"<User: ID={self.user_id} Username={self.username} Email={self.email}>"

class Picture(db.Model):
    __tablename__ = "pictures"
    
    pic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    pic_url = db.column(db.String, nullable=False)
    
    user = db.relationship("User", backref="pictures")
    
    def __repr__(self):
        return f"<Picture: pic_id={self.pic_id}"

class Conversation(db.Model):
    __tablename__ = "conversations"
    
    convo_id = db.column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    other_user = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", backref="conversations")
    
    def __repr__(self):
        return f"<Conversation between {self.user_id} and {self.other_user}"
    
class Messages(db.Model):
    __tablename__ = "messages"
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    convo_id = db.Column(db.Integer, db.ForeignKey("conversations.convo_id"), nullable=False)
    message = db.Column(db.String, nullable=False)
    
    convo = db.relationship("Conversation", backref="messages")
    
    def __repr__(self):
        return f"<Message={self.message_id}"
    
class User_Match(db.Model):
    __tablename__ = "user_matches"
    
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes = db.Column(db.Boolean)
    user_id = db.column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    liked = db.Column(db.Boolean)
    other_user = db.column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Connected to the db!")
    
if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)