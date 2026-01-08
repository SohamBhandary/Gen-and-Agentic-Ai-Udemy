from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = ""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    response = llm.invoke(state["user_query"])
    state["llm_output"] = response.content
    return state

def evaluation(state: State) -> Literal["chatbot_gemini", "endnode"]:
    if True:
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state: State):
    response = llm.invoke(state["user_query"])
    state["llm_output"] = response.content
    return state

def endnode(state: State):
    return state

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluation)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()
updated = graph.invoke({"user_query": "Hey what is 2 + 2?"})
print(updated)
