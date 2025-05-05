from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel
import os

load_dotenv()

""" Schema """
class DetectCallResponse(BaseModel):
    is_question_ai: bool

class CodingAIResponse(BaseModel):
    answer: str


client = wrap_openai(OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
))



class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

    
def detect_query(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is related
    to coding question or not.
    Return the response in specified JSON boolean only.
    """

    """Open AI call for the query detection is this query is coding or normal"""
    
    """Here i am using beta not chat,
       This only response in the defined structured,using pydantic
        DetectCallResponse in this class i decided the structured
    """
    result = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=DetectCallResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        ]
    )


    state["is_coding_question"]= result.choices[0].message.parsed.is_question_ai

    return state

def routing(state: State) -> Literal["solve_coding_question","solve_simple_question"]:
    is_coding_question = state.get("is_coding_question")

    if is_coding_question:
        return "solve_coding_question"
    else:
        return"solve_simple_question"


def solve_coding_question(state: State):
    user_message = state.get("user_message")
    
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to resolve the user query based on coding 
    problem he is facing
    """
    """Gemini Solve this question model 2.5 flash"""
    
    """Here i am using beta not chat,
       This only response in the defined structured,using pydantic
        CodingAIResponse in this class i decided the structured
    """
    result = client.beta.chat.completions.parse(
        model="gemini-2.0-flash", 
        response_format=CodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        ]
    )

    state["ai_message"]=result.choices[0].message.parsed.answer

    return state


def solve_simple_question(state: State):
    user_message = state.get("user_message")

    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to chat with user
    """

    """Gemini Solve this question model 1.5 flash"""

    result = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        response_format=CodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        ]
    )
    state["ai_message"] = result.choices[0].message.parsed.answer


    return state


graph_builder = StateGraph(State)

"""Node creation"""
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)

"""Edge Creation"""
graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges("detect_query", routing)
graph_builder.add_edge("solve_simple_question", END)
graph_builder.add_edge("solve_coding_question", END)


"""Complie the graph"""

graph = graph_builder.compile()



"""Useing the graph"""
def call_graph():
    state={
        "user_message":"Can you explain the pydantic",
        "is_coding_question":False,
        "ai_message":""
    }
    result = graph.invoke(state)

    print("Final Result is:  ", result)

call_graph()
