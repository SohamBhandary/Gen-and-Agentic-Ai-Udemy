# chat.py
import os
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI

# 🌟 STEP 1: Set your Gemini API key here (replace YOUR_API_KEY safely)
os.environ["GOOGLE_API_KEY"] = ""

# 🌟 STEP 2: Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # use "gemini-1.5-pro" for more intelligence
    temperature=0.7
)

# 🌟 STEP 3: Define the shared State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 🌟 STEP 4: Define your chatbot node
def chatbot(state: State):
    print("\n\nchatbot node running...")
    res = llm.invoke(state.get("messages"))  # send conversation so far
    return {"messages": [res.content]}  # append Gemini’s reply

# 🌟 STEP 5: Define another node
def samplenode(state: State):
    print("\n\nsample node running...")
    return {"messages": ["This is from sample node"]}

# 🌟 STEP 6: Build graph flow
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

# 🌟 STEP 7: Run the workflow
update = graph.invoke(State({"messages": ["Hi, my name is Soham"]}))
print("\n\n✅ Final updated state:\n", update)
