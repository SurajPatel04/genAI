from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.tools import tool
from typing import Literal
from langgraph.graph import StateGraph, START, END  
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import asyncio
load_dotenv()


@tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers and return the result."""
    return x * y


@tool
def add(x: int, y: int) -> int:
    """Add two numbers and return the result."""
    return x + y


llm = ChatGoogleGenerativeAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.0-flash",
)

# ----- 1. pydantic schema -----
class DetectCallResponse(BaseModel):
    is_coding_question: bool

class State(BaseModel):
    user_message: str
    ai_message: str
    is_coding_question: bool

def detect_query(state: State) -> State:
    user_message = state.user_message

    # Setup the output parser
    structured_llm = llm.with_structured_output(DetectCallResponse)


    # Use f-string to insert parser instructions
    system_prompt = f"""
    You are an AI assistant. Your job is to detect if the user's query is related
    to a coding question or not.
    """

    # Format messages
    msg = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]

    # Call the model
    result = structured_llm.invoke(msg)

    # Parse the result using the output parser

    # Return updated state
    return state.model_copy(update={"is_coding_question": result.is_coding_question})

def routing(state:State) -> Literal["solve_coding_question","solve_simple_question"]:
    is_coding_question = state.is_coding_question

    if is_coding_question:
        return "solve_coding_question"
    else:
        return "solve_simple_question"
    

def solve_coding_question(state: State):
    user_message = state.user_message
    
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to resolve the user query based on coding 
    problem he is facing
    """
    """Gemini Solve this question model 2.5 flash"""
    
    """Here i am using beta not chat,
       This only response in the defined structured,using pydantic
        CodingAIResponse in this class i decided the structured
    """
    msg = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=user_message)
    ]
    result = llm.invoke(msg)
    print(result.content)
    return state.model_copy(update={"ai_message":result.content})



def solve_simple_question(state: State):
    user_message = state.user_message
    tools = [multiply, add]

    SYSTEM_PROMPT = (
        """You are an AI assistant. If a question can be answered without any tool, answer directly.
Only call a tool when it is strictly necessary.""")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = executor.invoke({"input": user_message})
    answer = result["output"]

    return state.model_copy(update={"ai_message": answer})




graph_builder = StateGraph(State)

graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question",solve_simple_question)


graph_builder.add_edge(START,"detect_query")
graph_builder.add_conditional_edges("detect_query",routing)
graph_builder.add_edge("solve_simple_question",END)
graph_builder.add_edge("solve_coding_question",END)

graph = graph_builder.compile()

async def call_graph():
    state={
        "user_message":"write print hello in java program",
        "is_coding_question":False,
        "ai_message":""
    }

    result = await graph.ainvoke(state)

    print(result.get("ai_message"))


asyncio.run(call_graph())
