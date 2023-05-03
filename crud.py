from flask_login import current_user
from model import db, User, Picture, Message, connect_to_db

def get_all_users():
    return User.query.all()

def get_users_by_sex(is_female):
    return User.query.filter_by(is_female=is_female).all()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_user_id(id):
    return User.query.get(id)

def get_user_pics(id):
    return Picture.query.filter_by(user_id=id).all()

def get_pic_by_id(pic_id):
    return Picture.query.filter_by(pic_id=pic_id).first()

def create_user(username, password, user_bio, user_email, is_female):
    new_user = User(username=username, password=password, user_bio=user_bio, user_email=user_email, is_female=is_female)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_message_by_id(message_id):
    return Message.query.filter_by(message_id=message_id).first()

def get_all_messages(sender_id=None, recipient_id=None):
    if sender_id is not None and recipient_id is not None:
        return Message.query.filter_by(sender_id=sender_id, recipient_id=recipient_id).all()
    elif sender_id is not None:
        return Message.query.filter_by(sender_id=sender_id, recipient_id=current_user.id).all()
    elif recipient_id is not None:
        return Message.query.filter_by(sender_id=current_user.id, recipient_id=recipient_id).all()
    else:
        return Message.query.filter_by(recipient_id=current_user.id).all()