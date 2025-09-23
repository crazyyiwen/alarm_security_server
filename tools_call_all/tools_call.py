from datetime import datetime
from langchain_core.tools import tool
from typing import Dict, List
from fastapi import FastAPI
import requests

# ------------------ Memory ------------------
system_enabled = False
local_base_url = "http://localhost:8000/"
register_url = "http://localhost:5218/"

# ------------------ Tool functions ------------------

# ---- Define Tools ----
@tool
def arm_system(username: str) -> str:
    """Arm system by calling the API endpoint
    Args:
        username: The name of the user.
    """
    try:
        response = requests.post(
            f"{local_base_url}api/arm_ayatem",
            json={
                "username": username,
                "mode": '"away" | "home" | "stay"'
            }
        )
        response.raise_for_status()
        return response.json().get("status", "System armed")
    except Exception as e:
        return f"Error calling arm_ayatem API: {e}"

@tool
def disarm_system(username: str) -> str:
    """Disarm system by calling the API endpoint
    Args:
        username: The name of the user.
    """
    try:
        response = requests.post(
            f"{local_base_url}api/disarm_system",
            json={
                "username": username
            }
        )
        response.raise_for_status()
        return response.json().get("status", "System disarmed")
    except Exception as e:
        return f"Error calling disarm_system API: {e}"

@tool
def add_user(username: str, password: str, expire_from: str, expire_to: str) -> str:
    """Add user by calling the API endpoint.
    Args:
        username: The name of the user.
        password: A numeric PIN (4 digits).
        expire_from: Start time in ISO format (YYYY-MM-DD).
        expire_to: End time in ISO format (YYYY-MM-DD).
    """
    try:
        if username == "" or password == "":
            raise ValueError("Please provide valid username or password")
    except Exception as e:
        return f"Failed to parse input: {e}"

    try:
        res = requests.post(
            f"{register_url}api/Users/AddUser",  # same server
            json=
            {
                "id": 0,
                "name": username,
                "password": password,
                "start_time": expire_from,
                "end_time": expire_to,
                "isadminuser": False,
                "permissions": '["arm","disarm"]'
            }
        )
        st = res.raise_for_status()
        response = requests.post(
            f"{local_base_url}api/add_user",  # same server
            json={
                "username": username,
                "password": password,
                "start_time": expire_from,
                "end_time": expire_to
            }
        )
        response.raise_for_status()
        return response.json().get("status", "User added")
    except Exception as e:
        return f"Error calling add_user_api: {e}"

@tool
def remove_user(username: str) -> str:
    """Remove user by calling the API endpoint.
    Args:
        username: The name of the user.
    """
    try:
        if username == "":
            raise ValueError("Please provide valid username")
        elif username == "admin":
            return "You do not have access to remove admin user"
    except Exception as e:
        return f"Failed to parse input: {e}"

    try:
        response = requests.post(
            f"{local_base_url}api/remove_user",  # same server
            json={
                "username": username
            }
        )
        response.raise_for_status()
        return response.json().get("status", "User removed")
    except Exception as e:
        return f"Error calling remove_user_api: {e}"

@tool
def list_user() -> str:
    """List all the current valid users by calling the API endpoint.
    """
    try:
        response = requests.get(
            f"{local_base_url}api/list_users",  # same server
        )
        response.raise_for_status()
        return response.json().get("status", "All the valid users")
    except Exception as e:
        return f"Error calling list_users_api: {e}"

@tool
def door_operations(username: str, password: str, try_count: int) -> str:
    """Open door operations."""
    try:
        response = requests.post(
            f"{local_base_url}api/door_operation",
            json={
                "username": username,
                "password": password,
                "try_count": try_count
            }
        )
        response.raise_for_status()
        return response.json().get("status", "System armed")
    except Exception as e:
        return f"Error calling arm_ayatem API: {e}"
    
@tool
def default_tool(usermessage: str) -> str:
    """Default tool.
    Args:
        usermessage: this message is used for return.
    """
    try:
        return usermessage
    except Exception as e:
        return f"Error calling list_users_api: {e}"



