import os
from typing import List, TypedDict
import uuid
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.tools import StructuredTool
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.tracers import ConsoleCallbackHandler

from prompts.system_prompts import alarm_security_system_message
from system_setup.env_setup import set_env
from tools_call_all.tools_call import add_user, arm_system, default_tool, disarm_system, door_operations, list_user, remove_user


uid_str = str(uuid.uuid4())

# ------- Enable memory ---------------
class AgentState(TypedDict):
    messages: List[BaseMessage]
    result: str  


set_env()

# ---- Bind Tools to LLM ----
tools = [arm_system, disarm_system, add_user, remove_user, list_user, door_operations, default_tool]
llm = ChatOpenAI(model="gpt-4o", callbacks=[ConsoleCallbackHandler()]).bind_tools(tools)

# ---- Router Node ----
def router(state: AgentState):
    """LLM decides which tool to call and executes it."""
    messages = [SystemMessage(content=alarm_security_system_message)] + state["messages"]

    response = llm.invoke(messages)
    if response.tool_calls:
        tool_call = response.tool_calls[0]  # dict with tool info
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})

        # Find the tool object by name
        tool_map = {t.name: t for t in tools}  # tools list defined earlier

        if tool_name in tool_map:
            tool: StructuredTool = tool_map[tool_name]
            result = tool.invoke(tool_args)
            new_messages = state["messages"] + [AIMessage(content=result)]
            return {"messages": new_messages, "result": result}

    return {"result": "No valid tool selected."}

# ---- Build Graph ----
workflow = StateGraph(AgentState)
workflow.add_node("router", router)
workflow.add_edge("router", END)
workflow.set_entry_point("router")

# ---- Compile ----
app_graph = workflow.compile()