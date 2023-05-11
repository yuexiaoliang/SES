from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def create_mongo_client() -> MongoClient:
    return MongoClient('mongodb://localhost:27017')


def get_mongo_client() -> MongoClient:
    try:
        client = create_mongo_client()
        yield client
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        yield None
    finally:
        if 'client' in locals() and client is not None:
            client.close()
            print("Disconnected from MongoDB")
