import datetime
import math
import random
from joblib import Parallel, delayed
from pymongo import MongoClient
from fastapi import APIRouter, Depends
from models.stock import StockHistory
from models.trading_test import StockTestResponse, StocksTestResponse, StockSimulatedTrading
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


def trading(data,  raw_funds: float = 10000):
    '''模拟炒股测试
    :path code: 股票代码

    :param start_date: 开始日期
    :param end_date: 结束日期
    :param raw_funds: 初始资金，默认为 10000

    :return: 测试数据
    '''

    if (len(data) < 1): return

    stock_code = data[0]['stock_code']

    # 剩余资金
    balance = raw_funds

    result: StockSimulatedTrading = {
        'stock_code': stock_code,
        # 状态：long-持仓 short-空仓
        'status': 'short',
        # 持仓数量
        'holdings': 0,
        # 初始资金
        'raw_funds': raw_funds,
        # 盘中持仓时间
        'intraday_holding_time': 0,
        # 记录
        'records': []
    }

    try:
        for index, item in enumerate(data):
            if index < 2: continue

            prev = data[index - 1]
            print(index)
            opening = item['opening_price']
            closing = item['closing_price']
            date = item['date']

            # 买入
            if (result['status'] == 'short'):
                # 单价
                # 当日收盘价 + (当日收盘价 - 当日开盘价) * 阈值
                price = format_float(closing + (closing - opening) * random.random())

                # 买入股票数量（手）
                _count = math.floor(balance / (price * 100));
                # 买入股票数量（股）
                _count2 = _count * 100
                if (_count <= 0):
                    return;

                # 总金额
                total = calculateBuyCost(_count * price * 100);

                # 动态计算买入数量以及总额
                while (total > balance):
                    _count -= 1;
                total = calculateBuyCost(_count * price * 100);

                # 持仓
                result['holdings'] = _count2

                # 状态变为持仓
                result['status'] = 'long'

                result['records'].append({
                    'type': 'buy',
                    'date':  date,
                    'price': price,
                    'count': _count2,
                    'total': total
                })
            else:
                # 单价
                # 上一日收盘价 - (上一日收盘价 * 止损比例 + 上一日收盘价 * 阈值)
                stopLossRatio = -0.025
                prevClosing = prev['closing_price']
                price = format_float(prevClosing - (prevClosing * stopLossRatio + prevClosing * 0.003 * random.random()))

                # 盘中持仓时间
                result['intraday_holding_time'] += 1;

                # 卖出总金额
                total = calculateSellCost(price, result['holdings']);

                # 重置本金
                balance = format_float(balance + total);

                # 状态变为持仓
                result['status'] = 'short'

                result['records'].append({
                    'type': 'sell',
                    'date':  date,
                    'price': price,
                    'count': result['holdings'],
                    'total': total
                })
    except Exception as e:
        print(e)

    return result

def trading_generator(dataList, raw_funds):
    for item in dataList:
        data = trading(item, raw_funds)
        if len(data) > 0:
            yield data


@router.get('/single/{code}', name='单只股票模拟炒股测试', response_model=StockTestResponse)
def single_stock(code: str, start_date:str = '', end_date: str = '', raw_funds: float = 10000, client: MongoClient = Depends(get_mongo_client)):

    historyCollection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    query = {}

    if (start_date or end_date):
        query['date'] = {}

    if (start_date):
        query['date']['$gte'] = start_date

    if (end_date):
        query['date']['$lt'] = end_date

    if (code):
        query['stock_code'] = code

    cursor = historyCollection.find(query)

    # 查询结果为空时，返回默认值
    if not cursor:
        return {"message": "未找到符合条件的数据", "code": 0, "data": None}

    data = convert_list_objectid_to_str(list(cursor))

    return {
        'message': '获取成功',
        'code': 0,
        'data': {
            'records': trading(data, raw_funds),
            'raw_funds': raw_funds
        }
    }


@router.get('/stocks', name='多只股票模拟炒股测试', response_model=StocksTestResponse)
def multi_stocks(stocks , start_date:str = '', end_date: str = '', raw_funds: float = 10000, client: MongoClient = Depends(get_mongo_client)):
    historyCollection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    _codes = stocks.split(',')

    query = {
        'stock_code': { '$in': _codes }
    }

    if (start_date or end_date):
        query['date'] = {}

    if (start_date):
        query['date']['$gte'] = start_date

    if (end_date):
        query['date']['$lt'] = end_date

    pipeline = [
        {
            "$match": query
        },
        {
            '$group': {
                '_id': '$stock_code',  # 以 stock_code 作为分组依据
                'data': {'$push': '$$ROOT'}  # 将每个分组的文档保存到一个数组中
            }
        },
        {
            '$project': {
                '_id': 0,
                'data': 1
            }
        }
    ]

    dataList = historyCollection.aggregate(pipeline)
    dataList = [convert_list_objectid_to_str(item['data']) for item in dataList]


    def compute_task(item):
        data = trading(item, raw_funds)
        if len(data) > 0:
            return data

    # 并行计算，提高计算速度
    result = Parallel(n_jobs=-1)(delayed(compute_task)(item) for item in dataList)
    result = [data for data in result if data is not None]

    return {
        'message': '获取成功',
        'code': 0,
        'data': {
            'records': result,
            'raw_funds': raw_funds
        }
    }