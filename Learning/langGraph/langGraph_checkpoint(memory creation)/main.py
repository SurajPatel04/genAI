from graph import create_chat_graph
from dotenv import load_dotenv

# Import the MongoDB-backed checkpointer for saving checkpoints
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()
# Connection string for your MongoDB instance (replace credentials/host/port as needed)
#here admin is password and username also check docker file
MONGODB_URI = "mongodb://admin:admin@localhost:27018"


# Here 'thread_id' is set so each user session can be uniquely identified.
# here id should be uniuq so we can set user_id
config = {"configurable":{"thread_id":"2"}}

def init():
    # Create a MongoDBSaver that will manage saving/loading checkpoints,
    # using your connection string. The context manager ensures we clean up properly.
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        # Build the chat graph, passing in our MongoDB checkpointer.
        # This graph will use MongoDB to persist its state.
        graph_with_mongo=create_chat_graph(checkpointer=checkpointer)
        while True:
            user_input = input(">> ")
            for event in graph_with_mongo.stream({"messages":[{"role":"user","content":user_input}]},config,  stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()

init()
