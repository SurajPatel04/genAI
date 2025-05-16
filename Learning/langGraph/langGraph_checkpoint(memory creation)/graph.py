from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

"""

Not Working
client = OpenAI(api_key=os.getenv("GOOGLE_API_KEY"),
           base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

def ai(message):
    response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages = message
    )

    return response.choices[0].message.content

"""

llm = init_chat_model(model_provider="google_genai", model="gemini-2.0-flash")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
def chat(state: State):
    """
    messages=state.get("messages")
    response=llm.invoke(messages)
    return {"message": [response]}

    """
    return {"messages": [llm.invoke(state["messages"])]}

""" return {"messages": [llm.invoke(state["messages"])]} """

graph_builder = StateGraph(State)

graph_builder.add_node("chat", chat)
graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", END)

"""Without any memory"""
graph = graph_builder.compile()

"""Create a new graph with given checkpointer(memory)"""
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


