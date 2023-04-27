from pymongo import MongoClient
import efinance as ef

# 获取数据库
client = MongoClient('mongodb://localhost:27017')

# 获取集合
db = client.stock

# 采集沪深市场 A 股最新状况
stocks_df = ef.stock.get_realtime_quotes()
stocks_data = stocks_df.to_dict('records')
db.stocks.drop()
db.stocks.insert_many(stocks_data)
print('采集沪深市场 A 股最新状况完成！')

stock_codes = stocks_df['股票代码'].tolist()

# 采集沪深市场 A 股基本信息
base_info_df = ef.stock.get_base_info(stock_codes)
base_info_data = base_info_df.to_dict('records')
db.base_info.drop()
db.base_info.insert_many(base_info_data)
print('采集沪深市场 A 股基本信息完成！')


# 采集沪深市场 A 股日 K 线数据
stock_history_dict = ef.stock.get_quote_history(stock_codes)

db.stock_history.drop()
for key, value in stock_history_dict.items():
    print("表名:", key)
    stock_history_data = value.to_dict("records")
    db.stock_history.insert_many(stock_history_data)

print('采集沪深市场 A 股日 K 线数据完成！')

client.close()

