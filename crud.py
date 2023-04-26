from model import db, User, Picture, Conversation, Message, User_Match, connect_to_db

def get_all_users():
    return User.query.all()

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

def create_user(username, password, user_bio, user_email, is_female):
    new_user = User(username=username, password=password, user_bio=user_bio, user_email=user_email, is_female=is_female)
    return new_user

def get_messages_by_convo(convo_id):
    return Message.query.filter_by(convo_id = convo_id).all()

def get_all_convo():
    return Conversation.query.all()

def get_convo_by_id(convo_id):
    return Conversation.query.filter_by(convo_id = convo_id).first()