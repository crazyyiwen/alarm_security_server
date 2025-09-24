from fastapi import APIRouter, HTTPException, Query, Request
import asyncpg

from models.request_models import KnowledgeRequest
from services.db_services.db_knowledge_service import load_knowledge, save_knowledge


api_router = APIRouter()

#---- Get thread ----
@api_router.get("/api/get_knowledge_by_knowledge_id")
async def get_checkpoint_by_checkpoint_id(knowledge_id: str = Query(..., description="Thread ID to fetch"), request: Request = None):
    try:
        response = await load_knowledge(knowledge_id, request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
@api_router.post("/api/update_knowledge_by_knowledge_id/")
async def update_state_by_checkpoint_id(payload: KnowledgeRequest, request: Request = None):
    try:
        response = await save_knowledge(payload, request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
