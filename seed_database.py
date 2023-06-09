import os
import json

import crud
import model
import server

os.system("dropdb dating")
os.system("createdb dating")

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()
    
    with open('data/users.json') as f:
        user_data = json.loads(f.read())
        
    users_in_db = []

    for user in user_data:
        username, password,  user_bio, user_email, is_female = (user["username"], user["password"], user["user_bio"], user["user_email"], user["is_female"])
        db_user = crud.create_user(username, password, user_bio, user_email, is_female)
        users_in_db.append(db_user)
        
    model.db.session.add_all(users_in_db)
    model.db.session.commit()