import json

USERS_DB_FILE = "users_data.json"
HISTORY_DB_FILE = "history_data.json"

def load_users_database():
    try:
        with open(USERS_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_users_database(data):
    with open(USERS_DB_FILE, "w") as f:
        json.dump(data, f)

def load_history_database():
    try:
        with open(HISTORY_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": {}}

def save_history_database(data):
    with open(HISTORY_DB_FILE, "w") as f:
        json.dump(data, f)
