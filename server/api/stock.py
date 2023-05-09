from datetime import datetime, timedelta

import pymongo
from fastapi import APIRouter

from models.stock import StockResponse, StocksResponse

router = APIRouter()


@router.get('/list', name='获取股票列表', response_model=StocksResponse)
def get_stocks(page_size: int = 10, page_current: int = 1):
    client = pymongo.MongoClient('mongodb://localhost:27017')

    db = client.stock

    # 使用参数化查询，避免注入攻击
    cursor = db.stocks.find().skip((page_current - 1) * page_size).limit(page_size)

    # 查询结果为空时，返回默认值
    if not cursor:
        return {"message": "未找到符合条件的数据", "code": 0, "data": {
            "total": 0,
            "page_size": page_size,
            "page_current": page_current,
            "list": []
        }}

    result = list(cursor)

    # 将 ObjectId 对象转换为字符串
    for item in result:
        item['_id'] = str(item['_id'])

    total = db.stocks.count_documents({})

    # 返回数据
    return {"message": "获取成功", "code": 0, "data": {
        "total": total,
        "page_size": page_size,
        "page_current": page_current,
        "list": result
    }}


@router.get('/{code}', name='根据股票 code 获取股票信息', response_model=StockResponse)
def get_stock(code: str):
    client = pymongo.MongoClient('mongodb://localhost:27017')

    db = client.stock

    # 对 code 参数进行验证和过滤
    code = code.strip()
    if not code:
        return {"message": "code 参数不能为空", "code": 1, "data": None}

    # 使用参数化查询，避免注入攻击
    result = db.stocks.find_one({"code": {"$regex": code}})

    # 查询结果为空时，返回默认值
    if not result:
        return {"message": "未找到符合条件的数据", "code": 2, "data": None}

    # 将 ObjectId 对象转换为字符串
    result['_id'] = str(result['_id'])

    # 返回数据
    return {"message": "获取成功", "code": 0, "data": result}


@router.get('/daily-data/{code}', name='获取股票日线数据')
def get_daily_data(code: str, start_date: str = '', end_date: str = ''):
    ''' 获取股票日线数据

    :param start_date: 开始日期，如果不传则默认为 end_date 前 30 天

    :param end_date: 结束日期，如果不传则默认为当前时间

    :return: 股票日线数据
    '''

    if not code:
        return {"message": "code 参数不能为空", "code": 1, "data": None}

    current_time = datetime.now().date()

    if not end_date:
        # 获取当前日期
        end_date = current_time.strftime('%Y-%m-%d')

    if not start_date:
        # 计算10天前的日期
        start_date = (current_time - timedelta(days=30)).strftime('%Y-%m-%d')

    client = pymongo.MongoClient('mongodb://localhost:27017')

    db = client.stock

    query = {"code": {"$regex": code}, "date": {
        "$gt": start_date, "$lte": end_date}}
    cursor = db.stock_history.find(query)

    # 查询结果为空时，返回默认值
    if not cursor:
        return {"message": "未找到符合条件的数据", "code": 0, "data": []}

    result = list(cursor)

    # 将 ObjectId 对象转换为字符串
    for item in result:
        item['_id'] = str(item['_id'])

    return result
