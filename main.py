from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
# For messages
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

#Define the LLM model
model = init_chat_model(
    "gemini-3.6-flash",
    model_provider="google_genai"
)

# Designs the sate of the graph. AKA the info that will be carried through the graph
# MessagesState is a predefined class to handle messages and includes the role within the message like HumanMessage("What is Python?") | AIMessage("Python is...")
class State(MessagesState):
    pass

#Builds a graph whose state follows the State schema defined above. It creates the builder
builder = StateGraph(State)

#Creating a first note
def my_node(state):
    # get messages from state
    messages = state["messages"]
    # invoke model with those messages
    response = model.invoke(messages)
    # return state update
    return {"messages": [response]}

#Adding the node to the graph
builder.add_node("first-node", my_node)
builder.add_edge(START, "first-node")
builder.add_edge("first-node", END)

#compiles the graph
graph = builder.compile()

#Use the graph to run a conversation
#initialize the state with a human message
user_input = input("Ask a question: ")
initial_state={
    "messages": [
        HumanMessage(content=user_input)
    ]
}

#Runs the graph
result = graph.invoke(initial_state)

print("GRAPH RESULT:")
#print(result)

print("\nMESSAGES:")
for message in result["messages"]:
    print(type(message).__name__, ":", message.text)