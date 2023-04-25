from model import db, User, Picture, Conversation, Messages, User_Match, connect_to_db

def get_users_by_sex(is_female):
    return User.query.filter_by(is_female = is_female).all()

def get_user_by_username(username):
    return User.query.filter_by(username = username).first()

def get_user_by_user_id(user_id):
    return User.query.get(user_id)

def get_user_pics(user_id):
    return Picture.query.filter_by(user_id = user_id).all()

def get_pic_by_id(pic_id):
    return Picture.query.filter_by(pic_id = pic_id).first()