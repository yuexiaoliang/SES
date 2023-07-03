import datetime
import math
import random
from typing import Any
from joblib import Parallel, delayed
from pymongo import MongoClient
from fastapi import APIRouter, Depends, Body
from models.trading_test import SingleStockResponse, MultiStocksResponse, StockSimulatedTrading, MultiStocksRequest
from utils.format import convert_list_objectid_to_str
from utils.database import get_mongo_client
from utils.format import format_float
from constants.enums import DatabaseNames, DatabaseCollectionNames
from .stock import get_trade_dates, get_daily_data

# 止损比例
stopLossRatio = 0.03

router = APIRouter()

def calculate_transfer_fee(total: float):
    '''计算过户费'''
    return format_float(total * 0.00002)


def calculate_commission(total: float):
    '''计算佣金'''
    commission = format_float(total * 0.0003)
    return commission if commission > 5 else 5


def calculate_buy_cost(total: float):
    '''计算每股股票买入成本'''
    # 过户费
    transferFee = calculate_transfer_fee(total)

    # 佣金
    commission = calculate_commission(total)

    return format_float(transferFee + commission + total)


def calculate_sell_cost(price: float, count: int):
    '''计算卖出价格'''
    total = price * count

    # 计算印花税
    stampDuty = total * 0.001

    # 过户费
    transferFee = calculate_transfer_fee(total)

    # 佣金
    commission = calculate_commission(total)

    return format_float(total - stampDuty - transferFee - commission)


def calculate_days(start: str, end: str):
    '''计算持仓时间'''
    start_date_obj = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = end_date_obj - start_date_obj
    return  delta.days


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
        'records': [],
        # 现有资金
        'balance': raw_funds,
        # 市值
        'market_value': 0,
        # 总资产
        'total_funds': raw_funds
    }

    for index, item in enumerate(data):
        if index < 2: continue

        prev = data[index - 1]
        opening = item['opening_price']
        closing = item['closing_price']
        highest_price = item['highest_price']
        lowest_price = item['lowest_price']

        date = item['date']

        # 买入
        # 如果是空仓状态则进行买入操作
        if (result['status'] == 'short'):
            macd = item['macd']
            prevMacd = prev['macd']

            if (not macd or not prevMacd):
                continue

            rsi6 = item['rsi6']
            prevRsi6 = prev['rsi6']

            # RSI 是否上升
            # isRsiUp = rsi6 > item['rsi12'];
            isRsiUp = True

            # MACD 是否上升
            isMacdUp = macd > prevMacd;
            # isMacdUp = True


            # 价格是否上升（跌涨辐大于 2）
            # isPriceUp = prev['change_percent'] > 0
            isPriceUp = True

            # 买入条件成立
            isEstablish = isMacdUp and isPriceUp and isRsiUp

            if (not isEstablish):
                continue;

            # 单价
            # 当日收盘价 + (当日收盘价 - 当日开盘价) * 阈值
            price = format_float(closing + (closing - opening) * random.random())
            price = closing

            # 买入股票数量（手）
            _count = math.floor(result['balance'] / (price * 100));
            if (_count <= 0):
                continue;

            # 总金额
            total = calculate_buy_cost(_count * price * 100);

            # 动态计算买入数量以及总额
            while (total > result['balance']):
                _count = _count - 1;
                total = calculate_buy_cost(_count * price * 100);

            # 买入股票数量（股）
            _count2 = _count * 100
            # 持仓
            result['holdings'] = _count2

            # 状态变为持仓
            result['status'] = 'long'

            # 重置剩余资金
            result['balance'] = format_float(result['balance'] - total);

            # 买入当天则增加一天盘中持仓时间
            result['intraday_holding_time'] += 1;

            result['records'].append({
                'type': 'buy',
                'date':  date,
                'price': price,
                'count': _count2,
                'total': total,
                'balance': result['balance']
            })
        else:
            # 盘中持仓时间
            # 只要是持仓状态则增加一天盘中持仓时间
            result['intraday_holding_time'] += 1;


            ''' 卖出
            1. 动态亏损超过止损比率
            '''
            if item['change_percent'] > -stopLossRatio * 100:
                continue

            # 单价
            # 上一日收盘价 - (上一日收盘价 * 止损比例 + 上一日收盘价 * 阈值)
            prevClosing = prev['closing_price']
            price = format_float(prevClosing - (prevClosing * stopLossRatio))

            # 卖出总金额
            total = calculate_sell_cost(price, result['holdings']);

            # 重置剩余资金
            result['balance'] = format_float(result['balance'] + total);

            # 状态变为空仓
            result['status'] = 'short'

            result['records'].append({
                'type': 'sell',
                'date':  date,
                'price': price,
                'count': result['holdings'],
                'total': total,
                'balance': result['balance']
            })

            # 重置持仓数量
            result['holdings'] = 0

        # 计算市值
        if (result['holdings'] == 0):
            result['market_value'] = 0
        else:
            last = result['records'][-1]
            result['market_value'] = format_float(last['total'])

        # 计算总资产
        result['total_funds'] = format_float(result['balance'] + result['market_value'])

    return result


@router.get('/single/{code}', name='单只股票模拟炒股测试', response_model=SingleStockResponse)
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
        'data': trading(data, raw_funds)
    }


@router.post('/multi', name='多只股票模拟交易测试', response_model=MultiStocksResponse)
def multi_stocks(request: MultiStocksRequest = Body(...), client: MongoClient = Depends(get_mongo_client)):

    body = request.dict()

    codes, start_date, end_date, raw_funds = body['codes'], body['start_date'], body['end_date'], body['raw_funds']

    if (not codes):
        stock_collection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS.value]
        d = stock_collection.find({ 'latest_price': { '$gt': 1 } })
        codes = [item['stock_code'] for item in d]

    historyCollection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    query = {
        'stock_code': { '$in': codes }
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
    # 按照 total_funds 排序
    result = sorted(result, key=lambda item: item['total_funds'], reverse=True)

    return {
        'message': '获取成功',
        'code': 0,
        'data': result
    }

