from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.types import interrupt
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
import os


load_dotenv()

@tool()
def human_assitance_tool(query: str):
    # Description 
    """Request assitance from a human"""

    # Graph will exit out after saving data in DB
    human_response = interrupt({"query":query})

    # resume with the data
    return human_response["data"]


tools = [human_assitance_tool]

llm = init_chat_model(model_provider="google_genai", model="gemini-2.0-flash")

llm_with_tools = llm.bind_tools(tools=tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
def chat(state: State):
    message = llm_with_tools.invoke(state["messages"])

    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages":[message]}

""" return {"messages": [llm.invoke(state["messages"])]} """

graph_builder = StateGraph(State)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("chat", chat)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START, "chat")
graph_builder.add_conditional_edges(
    "chat",
    tools_condition
)
graph_builder.add_edge("tools","chat")
graph_builder.add_edge("chat", END)

"""Without any memory"""
graph = graph_builder.compile()

"""Create a new graph with given checkpointer(memory)"""
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


