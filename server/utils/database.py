from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_mongo_client() -> MongoClient:
    try:
        client = MongoClient('mongodb://localhost:27017')
        print("Connected to MongoDB")
        yield client
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        yield None
    finally:
        if 'client' in locals() and client is not None:
            client.close()
            print("Disconnected from MongoDB")
