from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from agent_v2.state import State
from agent_v2.llm import llm

from agent_v2.prompts import (
    CHAT_SYSTEM_MESSAGE,
    TASK_SYSTEM_MESSAGE,
    ROUTER_SYSTEM_MESSAGE
)

from agent_v2.tools import (
    create_task,
    list_tasks,
    delete_task,
    complete_task,
)

from agent_v2.agents.rag import rag_agent


# ----------------------
# State
# ----------------------



class Route(TypedDict):
    next: Literal[
        "conversation_agent",
        "task_agent",
        "rag_agent",
    ]


# ----------------------
# Tools
# ----------------------

tools = [
    create_task,
    list_tasks,
    delete_task,
    complete_task,
]

tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

router_llm = llm.with_structured_output(Route)


# ----------------------
# Router
# ----------------------
def get_route(user_message):

    decision = router_llm.invoke(
        [
            ROUTER_SYSTEM_MESSAGE,
            user_message,
        ]
    )

    print(f"Router -> {decision['next']}")

    return decision["next"]

def router(state: State):

    user_message = state["messages"][-1]

    return get_route(user_message)


# ----------------------
# Agents
# ----------------------

def conversation_agent(state: State):

    messages = [CHAT_SYSTEM_MESSAGE] + state["messages"]

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }


def task_agent(state: State):

    messages = [TASK_SYSTEM_MESSAGE] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# ----------------------
# Graph
# ----------------------

builder = StateGraph(State)

builder.add_node("conversation_agent", conversation_agent)
builder.add_node("task_agent", task_agent)
builder.add_node("rag_agent", rag_agent)
builder.add_node("tools", tool_node)

builder.add_conditional_edges(
    START,
    router,
    {
        "conversation_agent": "conversation_agent",
        "task_agent": "task_agent",
        "rag_agent": "rag_agent",
    },
)

builder.add_edge("conversation_agent", END)
builder.add_edge("rag_agent", END)

builder.add_conditional_edges(
    "task_agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "task_agent")

graph = builder.compile()