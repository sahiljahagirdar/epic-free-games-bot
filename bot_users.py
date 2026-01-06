import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return set()

    with open(USERS_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def user_exists(chat_id: int) -> bool:
    return chat_id in load_users()

def save_user(chat_id: int):
    users = load_users()
    users.add(chat_id)

    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

def get_all_users():
    return load_users()
