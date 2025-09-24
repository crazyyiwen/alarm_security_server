import os
from typing import Annotated, List, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import StructuredTool
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages

from prompts.system_prompts import alarm_security_system_init_message, alarm_security_system_router_message, alarm_security_system_pwd_message
from services.db_services.db_chat_service import load_history, save_message
from system_setup.env_setup import set_env
from tools_call_all.tools_call import add_user, arm_system, default_tool, disarm_system, door_operations, list_user, remove_user
import uuid

# ------- uuid ------------------------
uid_str = str(uuid.uuid4())


# ------- Enable memory ---------------
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    result: str 



checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": uid_str}}
workflow = StateGraph(AgentState)

set_env()

# ---- Bind Tools to LLM ----
tools = [arm_system, disarm_system, add_user, remove_user, list_user, door_operations, default_tool]
llm = init_chat_model("openai:gpt-4.1")
llm_with_tools = llm.bind_tools(tools)

# ---- Router Node ----
async def router(state: AgentState):
    """LLM decides which tool to call and executes it."""
    messages = [SystemMessage(content=alarm_security_system_router_message)] + state["messages"]

    response = await llm_with_tools.ainvoke(messages, config)
    if response.tool_calls:
        tool_call = response.tool_calls[0]  # dict with tool info
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        # Find the tool object by name
        tool_map = {t.name: t for t in tools}  # tools list defined earlier

        if tool_name in tool_map:
            tool: StructuredTool = tool_map[tool_name]
            result = await tool.ainvoke(tool_args)
            return {"messages": [AIMessage(content=result)], "result": result}

    return {"result": "No valid tool selected."}

# ---- Normal Chat Node ----
async def normal_chat(state: AgentState):
    """Mormal chat."""
    messages = state["messages"]
    response = await llm_with_tools.ainvoke(messages, config)
    return {"messages": [AIMessage(content=response.content)], "result": response.content}

# ---- Operation Node ----
async def operation(state: AgentState):
    """Users do operation."""
    messages = state["messages"]
    return {"messages": [AIMessage(content="operation")], "result": messages[0].content}

# ---- Operation Node ----
async def evaluator(state: AgentState):
    """Evaluate the pwd."""
    messages = [SystemMessage(content=alarm_security_system_pwd_message)] + state["messages"]
    response = await llm_with_tools.ainvoke(messages, config)
    return {"messages": [AIMessage(content=response.content)], "result": response.content}

# ---- Init Node ----
async def init(state: AgentState):
    """LLM decides normal char， routing operation."""
    messages = [SystemMessage(content=alarm_security_system_init_message)] + state["messages"]
    response = await llm_with_tools.ainvoke(messages, config)
    return {"result": response.content}

# ---- Gateway Node(Reusable node) ----
async def gateway(state: AgentState):
    """Conditional check."""
    return state["result"]

async def saving_point(state: AgentState):
    """Saving chat in db"""
    save_message(uid_str, {"messages": str(state["messages"])})
    # chat_history = load_history(uid_str)
    return

# ---- Build Graph ----
workflow.add_edge(START, "init")
workflow.add_conditional_edges("init", gateway, {"normal_chat": "normal_chat", "router": "router", "operation":"operation"})
workflow.add_node("init", init)
workflow.add_node("router", router)
workflow.add_node("normal_chat", normal_chat)
workflow.add_node("operation", operation)
workflow.add_node("evaluator", evaluator)
workflow.add_node("saving_point", saving_point)
workflow.add_edge("operation", "evaluator")
workflow.add_conditional_edges("evaluator", 
    gateway,
    {
        "accepted": END,
        "retry": END,
        "rejected": END
    })
workflow.add_edge("normal_chat", "saving_point")
workflow.add_edge("saving_point", END)
workflow.add_edge("router", END)


# ---- Compile ----
app_graph = workflow.compile(checkpointer=checkpointer)