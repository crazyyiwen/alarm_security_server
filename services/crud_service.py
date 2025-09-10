import json
import os

FILENAME = "alarm_user_management.json"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILEPATH = os.path.join(PROJECT_ROOT, "mock_db", FILENAME)

def load_users():
    """Load users from local JSON file."""
    try:
        if os.path.exists(FILEPATH):
            with open(FILEPATH, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        return f"Open user json failed: {e}"

def add_user_process(request):
    """Add a user to the local JSON file."""
    users = load_users()
    if request['name'] in users:
        return f"User '{request['name']}' already exists."

    users[request['name']] = request
    save_users_process(users)
    return f"User '{request['name']}' added."

def delete_user_process(username: str):
    """Delete a user from the local JSON file."""
    users = load_users()
    if username not in users:
        return False

    del users[username]
    save_users_process(users)
    return f"User '{username}' deleted."

def load_all_users():
    """Load all users from the local JSON file."""
    users = load_users()
    if len(users) != 0:
        return users
    else:
        return {}
    
def user_exist_check(username: str):
    """Check if user added in the json file."""
    users = load_users()
    if len(users) != 0:
        return username in users
    else:
        return False

def save_users_process(users: dict):
    """Save users to local JSON file."""
    with open(FILEPATH, "w") as f:
        json.dump(users, f, indent=4)