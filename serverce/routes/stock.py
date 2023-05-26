from datetime import datetime, timedelta

from pymongo import MongoClient
from fastapi import APIRouter, Depends

from models.stock import StockResponse, StocksResponse, StockHistoryResponse, ReportDatesResponse
from utils.format import convert_list_objectid_to_str, convert_dict_objectid_to_str
from utils.database import get_mongo_client
from constants.enums import DatabaseCollectionNames, DatabaseNames

router = APIRouter()


@router.get('/list', name='获取股票列表', response_model=StocksResponse)
def get_stocks(page_size: int = 10, page_current: int = 1, client: MongoClient = Depends(get_mongo_client)):
    stocks = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS.value]

    # 使用参数化查询，避免注入攻击
    cursor = stocks.find().skip((page_current - 1) * page_size).limit(page_size)

    # 查询结果为空时，返回默认值
    if not cursor:
        return {"message": "未找到符合条件的数据", "code": 0, "data": {
            "total": 0,
            "page_size": page_size,
            "page_current": page_current,
            "list": []
        }}

    result = list(cursor)

    total = stocks.count_documents({})

    # 返回数据
    return {"message": "获取成功", "code": 0, "data": {
        "total": total,
        "page_size": page_size,
        "page_current": page_current,
        "list": convert_list_objectid_to_str(result)
    }}


@router.get('/{code}', name='根据股票 code 获取股票信息', response_model=StockResponse)
def get_stock(code: str, client: MongoClient = Depends(get_mongo_client)):
    stocks = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS.value]

    # 对 code 参数进行验证和过滤
    code = code.strip()
    if not code:
        return {"message": "code 参数不能为空", "code": 1, "data": None}

    # 使用参数化查询，避免注入攻击
    result = stocks.find_one({"code": {"$regex": code}})

    # 查询结果为空时，返回默认值
    if not result:
        return {"message": "未找到符合条件的数据", "code": 2, "data": None}

    # 返回数据
    return {"message": "获取成功", "code": 0, "data": convert_dict_objectid_to_str(result)}


@router.get('/daily-data/{code}', name='获取股票日线数据', response_model=StockHistoryResponse)
def get_daily_data(code: str, start_date: str = '', end_date: str = '', client: MongoClient = Depends(get_mongo_client)):
    ''' 获取股票日线数据

    :param start_date: 开始日期，如果不传则默认为 end_date 前 30 天

    :param end_date: 结束日期，如果不传则默认为当前时间

    :return: 股票日线数据
    '''

    if not code:
        return {"message": "code 参数不能为空", "code": 1, "data": None}

    current_time = datetime.now().date()

    stock_history = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    if not end_date:
        # 获取当前日期
        end_date = current_time.strftime('%Y-%m-%d')

    if not start_date:
        # 计算10天前的日期
        start_date = (current_time - timedelta(days=30)).strftime('%Y-%m-%d')

    query = {"code": {"$regex": code}, "date": {
        "$gt": start_date, "$lte": end_date}}
    cursor = stock_history.find(query)

    # 查询结果为空时，返回默认值
    if not cursor:
        return {"message": "未找到符合条件的数据", "code": 0, "data": []}

    result = list(cursor)

    return {
        "message": "获取成功",
        "code": 0,
        "data": convert_list_objectid_to_str(result)
    }


@router.get('report_dates', name='获取股票财报日期', response_model=ReportDatesResponse)
def get_report_dates(client: MongoClient = Depends(get_mongo_client)):
    ''' 获取股票财报日期

    :return: 财报日期
    '''

    stock_report_dates = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.REPORT_DATES.value]

    # 使用参数化查询，避免注入攻击
    cursor = stock_report_dates.find()
    result = list(cursor)

    # 查询结果为空时，返回默认值
    if not result:
        return {"message": "未找到符合条件的数据", "code": 1, "data": None}

    # 返回数据
    return {"message": "获取成功", "code": 0, "data": convert_list_objectid_to_str(result)}