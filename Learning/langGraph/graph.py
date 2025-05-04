from typing_extensions import TypedDict
from langgraph.graph import StateGraph, Start

class State(TypedDict):
    user_message: str
    ai_message: str
    is_coding_question: bool

    
def detect_query(state: State):
    user_message = state.get("user_message")

    """Open AI call for the query detection is this query is coding or normal"""


    state.is_coding_question= True

    return state

def solve_coding_question(state: State):
    user_message = state.get("user_message")

    """Gemini Solve this question model 2.5 flash"""


    state.ai_message="Here your coding question answer"

    return state


def solve_simple_question(state: State):
    user_message = state.get("user_message")

    """Gemini Solve this question model 1.5 flash"""


    state.ai_message="Here your query answer"

    return state

"""Node creation"""
graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)

"""Edge Creation"""
