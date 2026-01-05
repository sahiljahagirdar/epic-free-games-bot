import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return set()
    with open(USERS_FILE, "r") as f:
        return set(json.load(f))

def save_user(chat_id):
    users = load_users()
    users.add(chat_id)
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

def get_all_users():
    return load_users()
