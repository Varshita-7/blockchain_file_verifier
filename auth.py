import json
import hashlib
import os

USERS_FILE = "users.json"

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def load_users():

    if not os.path.exists(USERS_FILE):

        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def signup(username, password):

    users = load_users()

    if username in users:
        return False

    users[username] = hash_password(password)

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    return True

def login(username, password):

    users = load_users()

    return (
        username in users
        and
        users[username]
        ==
        hash_password(password)
    )