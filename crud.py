from model import db, User, Picture, Conversation, Messages, User_Match, connect_to_db

def get_users():
    return User.query.all()

def get_user_by_username(username):
    return User.query.filter_by(username = username).first()

def get_user_by_user_id(user_id):
    return User.query.get(user_id)