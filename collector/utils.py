# 批量更新或插入数据
def update_df(df, col):
    data = df.to_dict('records')

    # 将 data 列表转换成以股票代码为键的字典
    update = {}
    for doc in data:
        stock_code = doc.pop('股票代码')
        update[stock_code] = doc

    # 批量更新或插入数据
    query = {"股票代码": {"$in": df['股票代码'].tolist()}}
    col.update_many(query, {"$set": update}, upsert=True)

# 更新或插入数据
def update_series(series, col):

    records = series.to_dict()

    col.update_many({"股票代码": {"$in": series['股票代码'].tolist()}}, {"$set": records}, upsert=True)
