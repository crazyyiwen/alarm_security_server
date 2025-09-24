from datetime import datetime
from typing import Dict
from fastapi import APIRouter, HTTPException, Query
from langchain_core.messages import HumanMessage


from services.llm_build_service import app_graph

api_router = APIRouter()


#---- Get thread ----
@api_router.get("/api/get_current_state_by_thread_id")
async def get_current_state_by_thread_id(thread_id: str = Query(..., description="Thread ID to fetch")):
    try:
        # Build config with thread_id
        config = {"configurable": {"thread_id": thread_id}}
        thread_data_1 = await app_graph.aget_state(config)
        return {
            "message": f"Thread state retrieved for thread_id={thread_id}",
            "thread_data": thread_data_1,
            "time_started": "Alarm Security System Agent is running well",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@api_router.get("/api/get_chat_history_thread_id")
async def get_chat_history_thread_id(thread_id: str = Query(..., description="Thread ID to fetch")):
    try:
        # Build config with thread_id
        config = {"configurable": {"thread_id": thread_id}}
        chat_history = list(await app_graph.aget_state_history(config))
        return {
            "message": f"Thread state retrieved for thread_id={thread_id}",
            "thread_data": chat_history,
            "time_started": "Alarm Security System Agent is running well",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---- Get thread ----
@api_router.get("/api/get_checkpoint_by_checkpoint_id")
async def get_checkpoint_by_checkpoint_id(thread_id: str = Query(..., description="Thread ID to fetch"), checkpoint_id: str = Query(..., description="Checkpoint ID to fetch")):
    try:
        # Build config with thread_id
        config = {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}
        state_data = await app_graph.aget_state(config)

        return {
            "message": f"Thread state retrieved for thread_id={thread_id}, checkpoint_id={checkpoint_id}",
            "state_data": state_data,
            "time_started": "Alarm Security System Agent is running well",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@api_router.post("/api/update_state_by_checkpoint_id")
async def update_state_by_checkpoint_id(thread_id: str = Query(..., description="Thread ID to fetch")):
    try:
        config = {"configurable": {"thread_id": thread_id}}
        # One pending issue - not able to update result, lacking reducer
        await app_graph.aupdate_state(
            config,
            {
                "messages": [HumanMessage(content="test for update")]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
