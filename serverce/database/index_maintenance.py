from utils.database import create_mongo_client
import pymongo


def create_index():
    client = create_mongo_client()
    collection = client['stock']['stocks_history']

    # 以股票代码创建索引
    collection.create_index([('stock_code', pymongo.DESCENDING)])
    collection.create_index([('date', pymongo.DESCENDING)])
    collection.create_index([('macd', pymongo.DESCENDING)])
    collection.create_index([('rsi6', pymongo.DESCENDING)])


if __name__ == "__main__":
    create_index()
