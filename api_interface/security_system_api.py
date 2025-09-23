from datetime import datetime
from typing import Dict
from fastapi import APIRouter, HTTPException
import requests

from langchain_core.messages import HumanMessage

from models.request_models import AddUserRequest, ArmRequest, DisarmRequest, DoorOperationRequest, QueryRequest, RemoveUserRequest
from models.state_models import AgentState
from services.crud_service import add_user_process, delete_user_process, load_all_users, user_exist_check
from services.llm_build_service import app_graph, uid_str

api_router = APIRouter()

password_attempts: Dict[str, int] = {}
chat_sessions: Dict[str, AgentState] = {}

#---- Do health check ----
@api_router.get("/healthcheck")
def health_check():
    time_zone = str(datetime.now())
    return {
        "message": f"Current time zone {time_zone}",
        "time_started": f'Alarm Security System Agent is running well',
        "Version": "1.0.0"
    }
    
#---- Arm system ----
@api_router.post("/api/arm_ayatem")
def enable_system_api(request: ArmRequest):
    if user_exist_check(request.username):
        return {"status": "System Armed"}
    else:
        return {"status": "Arm system failed, user is invalid"}
#---- Disarm system ----
@api_router.post("/api/disarm_system")
def disable_system_api(request: DisarmRequest):
    if user_exist_check(request.username):
        return {"status": "System disarmed"}
    else:
        return {"status": "Disarm system failed, user is invalid"}

#---- Add user API ----
@api_router.post("/api/add_user")
def add_user_api(request: AddUserRequest):
    users = {}
    users[request.username] = {
        "name": request.username,
        "password": request.password,
        "start_time": datetime.fromisoformat(request.start_time).isoformat(),
        "end_time": datetime.fromisoformat(request.end_time).isoformat(),
        "permissions": ["arm", "disarm"]
    }
    add_user_process(users[request.username])
    return {"status": f"User {request.username} added"}

#---- Remove user API ----
@api_router.post("/api/remove_user")
def remove_user_api(request: RemoveUserRequest):
    is_deleted =delete_user_process(request.username)
    if is_deleted:
        return {"status": f"User {request.username} removed"}
    else:
        return {"status": f"User {request.username} not found"}

#---- List all users API ----
@api_router.get("/api/list_users")
def list_users_api():
    valid_users = load_all_users()
    if len(valid_users) != 0:
        usernames = list(valid_users.keys())
        result = ", ".join(usernames)
        return {"status": result}
    else:
        return {"status": ""}

#---- Door operation API ----
@api_router.post("/api/door_operation")
def door_operation_api(request: DoorOperationRequest):
    valid_users = load_all_users()
    if request.try_count >= 2:
        return {"status": "Invalid password - locked"}
    if request.username in valid_users:
        userdetails = valid_users[request.username]
        if userdetails['password'] == request.password:
            return {"status": "Door opened"}
        else:
            return {"status": "Password incorrect, please try again"}
    else:
        return {"status": "Invalid user"}
    
#---- Query API for client side ----
@api_router.post("/chat")
def query_agent(request: QueryRequest):
    try:
        session_id = getattr(request, "session_id", "default")
        state = chat_sessions.get(session_id, {"messages": [], "result": ""})
        config = {"configurable": {"thread_id": uid_str}}
        state["messages"].append(HumanMessage(content=request.user_input))
        result = app_graph.invoke(state, config)
        chat_sessions[session_id] = result
        return {
            "reply": result["result"],
            "history": [m.content for m in result["messages"]],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))