from utils.database import create_mongo_client
import pymongo


def create_index():
    client = create_mongo_client()
    collection = client['stock']['stocks_history']

    # 以股票代码创建索引
    collection.create_index([('stock_code', pymongo.ASCENDING)])


if __name__ == "__main__":
    create_index()