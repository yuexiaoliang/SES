import datetime
import random
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import APIRouter, Depends
from models.stock import StockResponse, StockHistoryResponse
from utils.format import convert_list_objectid_to_str
from utils.database import get_mongo_client
from utils.format import format_float
from constants.enums import DatabaseNames, DatabaseCollectionNames

router = APIRouter()


def calculateTransferFee(total: float):
    '''计算过户费'''
    return format_float(total * 0.00002)


def calculateCommission(total: float):
    '''计算佣金'''
    commission = format_float(total * 0.0003)
    return commission if commission > 5 else 5


def calculateBuyCost(total: float):
    '''计算每股股票买入成本'''
    # 过户费
    transferFee = calculateTransferFee(total)

    # 佣金
    commission = calculateCommission(total)

    return format_float(transferFee + commission + total)


def calculateSellCost(price: float, count: int):
    '''计算卖出价格'''
    total = price * count

    # 计算印花税
    stampDuty = total * 0.001

    # 过户费
    transferFee = calculateTransferFee(total)

    # 佣金
    commission = calculateCommission(total)

    return format_float(total - stampDuty - transferFee - commission)


def calculateDays(start: str, end: str):
    '''计算持仓时间'''
    start_date_obj = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = end_date_obj - start_date_obj
    return  delta.days


def calculatePrice(item):
    '''计算单价
    模拟可能的买入、卖出价格
    '''
    opening = item['opening_price']
    closing = item['closing_price']
    return format_float(opening + (opening - closing) * random.random())
    # return item.closing_price


@router.get('/', name='模拟炒股测试', response_model=StockHistoryResponse)
def test_all(code: str = '', start_date:str = '', end_date: str = '', raw_funds: float = 10000, client: MongoClient = Depends(get_mongo_client)):
    '''模拟炒股测试

    :param start_date: 开始日期

    :param end_date: 结束日期

    :param code: 股票代码

    :param raw_funds: 初始资金，默认为 10000

    :return: 测试数据
    '''
    # historyCollection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    query = {}

    if (start_date or end_date):
        query['date'] = {}

    if (start_date):
        query['date']['$gte'] = start_date

    if (end_date):
        query['date']['$lt'] = end_date

    if (code):
        query['stock_code'] = code

    # cursor = historyCollection.find(query)

    # 查询结果为空时，返回默认值
    # if not cursor:
    #     return {"message": "未找到符合条件的数据", "code": 0, "data": []}

    # _list = list(cursor)

    # 所有持仓的股票 - {code: 总数}
    holding_stocks = []

    # 剩余资金
    balance = raw_funds


    ''' 买入
    - 从开始日期开始，每天筛选所有符合买入条件的股票
    - 并从筛选出的股票中随机（暂定）选择一只股票买入
    - 记录股票代码、股票名称、买入日期、单价、数量、佣金、过户费、总价、剩余资金
    '''

    ''' 卖出
    - 每天计算所持有的股票是否符合卖出条件，如果符合卖出条件，则卖出
    - 记录股票代码、股票名称、卖出日期、单价、数量、佣金、过户费、印花税、总收益（亏损）、所卖股票剩余持仓、剩余资金
    '''

    ''' 结果
    - 将所有的买入、卖出记录按日期排序
    '''

    return {
        'message': '获取成功',
        'code': 200,
        # 'data': convert_list_objectid_to_str(_list)
        'data': []
    }
