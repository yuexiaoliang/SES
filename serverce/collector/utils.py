from utils.database import create_mongo_client
from constants.enums import DatabaseCollectionNames, DatabaseNames

def create_client(name):
    """ 创建数据库客户端 """

    client = create_mongo_client()
    database = client[DatabaseNames.STOCK.value]

    collection = database[DatabaseCollectionNames[name].value]

    return [collection, client]