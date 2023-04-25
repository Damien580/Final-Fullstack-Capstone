import os
import json
from random import choice, randint
from datetime import datetime

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
    username, user_bio, user_email = (user["username"], user["user_bio"], user["user_email"])
    