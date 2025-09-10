# --- Request model ---
from openai import BaseModel


class QueryRequest(BaseModel):
    user_input: str

class AddUserRequest(BaseModel):
    username: str
    password: str
    start_time: str
    end_time: str

class RemoveUserRequest(BaseModel):
    username: str

class DoorOperationRequest(BaseModel):
    username: str
    password: str
    try_count: int

class ArmRequest(BaseModel):
    username: str
    mode:str

class DisarmRequest(BaseModel):
    username: str