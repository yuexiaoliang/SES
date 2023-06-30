import datetime
import math
import random
from typing import Any
from joblib import Parallel, delayed
from pymongo import MongoClient
from fastapi import APIRouter, Depends, Body
from models.trading_test import SingleStockResponse, MultiStocksResponse, StockSimulatedTrading, MultiStocksRequest, MultiHybridStocksResponse
from utils.format import convert_list_objectid_to_str
from utils.database import get_mongo_client
from utils.format import format_float
from constants.enums import DatabaseNames, DatabaseCollectionNames
from .stock import get_trade_dates, get_daily_data

# 止损比例
stopLossRatio = -0.025

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
        date = item['date']

        # 买入
        # 如果是空仓状态则进行买入操作
        if (result['status'] == 'short'):
            macd = item['macd']
            prevMacd = prev['macd']

            # if (not macd or not prevMacd):
            #     continue

            rsi6 = item['rsi6']
            prevRsi6 = prev['rsi6']

            # RSI 是否上升
            # isRsiUp = rsi6 > prevRsi6;
            isRsiUp = True

            # MACD 是否上升
            # isMacdUp = macd > prevMacd;
            isMacdUp = True


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
            if item['change_percent'] > stopLossRatio * 100:
                continue

            # 单价
            # 上一日收盘价 - (上一日收盘价 * 止损比例 + 上一日收盘价 * 阈值)
            prevClosing = prev['closing_price']
            price = format_float(prevClosing - (prevClosing * stopLossRatio + prevClosing * 0.003 * random.random()))

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

    return {
        'message': '获取成功',
        'code': 0,
        'data': result
    }


@router.post('/multi-hybrid', name='多只股票混合模拟交易测试', response_model=MultiHybridStocksResponse)
def multi_stocks(request: MultiStocksRequest = Body(...), client: MongoClient = Depends(get_mongo_client)):
    ''' 从 start_date 开始，到 end_date 结束，每天都进行一次模拟炒股。
    如果是空仓状态，则剔除当天不符合条件的股票，然后进行买入，如果没有合适的股票，则进入下一天。
    如果是持仓状态，则判断是否需要卖出，不需要则进入下一天。

    一、如果用户没有指定股票代码，则获取所有股票代码

    二、获取 start_date 到 end_date 之间的所有交易日

    三、交易日循环

    3.1 如果是持仓状态，则判断持仓股票是否有需要卖出的，有则卖出，没有则进入下一步。

    3.2 不管是空仓还是持仓状态，如果手中可用资金超过 2000 元则准备交易。首先剔除当天不符合买入条件的股票，然后对符合条件的股票进行随机买入，如果没有合适的股票，则进入下一天（下一个循环）。

    3.2.1 获取在 codes 中的股票数据

    3.2.2 判断基本买入条件，并买入

    - 较前一日跌涨幅（change_percent）大于 2%
    - 较前一日 macd 大于前两日 macd
    - 较前一日的 rsi6 小于 10
    '''

    body = request.dict()

    codes, start_date, end_date, raw_funds = body['codes'], body['start_date'], body['end_date'], body['raw_funds']

    if (not codes):
        stock_collection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS.value]
        codes = [item['stock_code'] for item in stock_collection.find()]

    # 所有交易日
    trade_dates = get_trade_dates(client)
    trade_dates = sorted(trade_dates['data'], key=lambda x: x)

    # 如果没有开始时间，则选择最小的时间作为开始时间
    if not start_date:
        start_date = min(trade_dates)

    # 如果没有结束时间，则选择最大的时间作为结束时间
    if not end_date:
        end_date = max(trade_dates)

    # 选择开始时间到结束时间中间的所有时间
    date_list = [time for time in trade_dates if start_date <= time <= end_date]
    date_list = sorted(date_list, key=lambda x: x)

    result = {
        'holdings_stocks': [],
        'status': 'long',
        'market_value': 0,
        'raw_funds': raw_funds,
        'balance': raw_funds,
        'total_funds': raw_funds,
        'records': {}
    }

    for date in date_list:
        date_index = trade_dates.index(date)
        # 计算 start_date
        _start_date = trade_dates[date_index - 5]
        # 计算 end_date
        _end_date = date


        # 如果是持仓状态，则判断持仓股票是否有需要卖出的，有则卖出，没有则进入下一步。
        if (result['status'] == 'long'):
            # 临时保存没有卖空的股票，循环完成后，再赋值给 result['holdings_stocks']
            holdings_stocks = []

            for stock in result['holdings_stocks']:
                # 获取股票历史数据
                history = get_daily_data(stock['stock_code'], start_date=_start_date, end_date=_end_date, client=client)
                history = history['data']

                # 获取当前股票的索引
                record_index = [index for index, item in enumerate(history) if item['date'] == date]
                if not record_index:
                    continue
                record_index = record_index[0]
                history_record = history[record_index]
                prev_history_record = history[record_index - 1]

                # 如果不符合卖出条件，则进入下一个循环
                if history_record['change_percent'] > stopLossRatio * 100:
                    holdings_stocks.append(stock)
                    continue

                # 单价
                # 上一日收盘价 - (上一日收盘价 * 止损比例 + 上一日收盘价 * 阈值)
                prevClosing = prev_history_record['closing_price']
                price = format_float(prevClosing - (prevClosing * stopLossRatio + prevClosing * 0.003 * random.random()))

                # 卖出数量
                sell_count = stock['holdings']
                # 重置持仓数量
                stock['holdings'] = stock['holdings'] - sell_count
                # 卖出总金额
                total = calculate_sell_cost(price, sell_count);
                # 重置剩余资金
                result['balance'] = format_float(result['balance'] + total);
                # 如果当前股票持仓状态为零则是清仓，否则是卖出
                type = 'clear' if stock['holdings'] == 0 else 'sell'
                # 本次交易记录
                stock_record = {
                    'type': type,
                    'date':  date,
                    'price': price,
                    'count': sell_count,
                    'total': total,
                    'balance': result['balance']
                }
                # 如果股票是持股状态，交易记录中对应股票的第 0 条记录必定是对应的买入记录
                stock_records = result['records'][stock['stock_code']][0]
                stock_records.append(stock_record)

                # 如果没有卖空则还是持仓状态，append 到持仓股票列表中
                if (stock_record['type'] != 'clear'):
                    holdings_stocks.append(stock)

            # 将没有卖出的股票赋值给 result['holdings_stocks']
            result['holdings_stocks'] = holdings_stocks

        # 不管是空仓还是持仓状态，如果手中可用资金超过 2000 元则准备交易。首先剔除当天不符合买入条件的股票，然后对符合条件的股票进行随机买入，如果没有合适的股票，则进入下一天（下一个循环）。
        if (result['balance'] < 2000):
            continue

        for code in codes:
            # 获取股票历史数据
            history = get_daily_data(code, start_date=_start_date, end_date=_end_date, client=client)
            history = history['data']

            # 获取当前股票的索引
            record_index = [index for index, item in enumerate(history) if item['date'] == date]
            if (not record_index):
                continue
            record_index = record_index[0]
            # 当前日数据
            history_record = history[record_index]
            # 上一日数据
            prev_history_record = history[record_index - 1]

            if (not history_record or not prev_history_record):
                continue

            macd = history_record['macd']
            prevMacd = prev_history_record['macd']

            if (not macd or not prevMacd):
                continue

            rsi6 = history_record['rsi6']
            prevRsi6 = prev_history_record['rsi6']

            # 是否超卖状态
            # isOversold = rsi6 > prevRsi6;
            isOversold = True

            # MACD 是否上升
            # isMacdUp = macd > prevMacd;
            isMacdUp = True

            # 价格是否上升（跌涨辐大于 0）
            # isPriceUp = prev_history_record['change_percent'] > 2
            isPriceUp = True

            # 买入条件是否成立
            isEstablish = isMacdUp and isPriceUp and isOversold

            if (not isEstablish):
                continue;

            # 从 result['holdings_stocks'] 中找出当前股票
            # 如果找不到则说明是新股票，需要初始化
            stock = [item for item in result['holdings_stocks'] if item['stock_code'] == code]
            if (len(stock) == 0):
                stock = {
                    'stock_code': code,
                    'stock_name': history_record['stock_name'],
                    'holdings': 0
                }
            else:
                stock = stock[0]

            opening = history_record['opening_price']
            closing = history_record['closing_price']

            # 单价
            # 当日收盘价 + (当日收盘价 - 当日开盘价) * 阈值
            price = format_float(closing + (closing - opening) * random.random())
            stock['price'] = price

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

            if (_count <= 0):
                continue;

            # 买入股票数量（股）
            _count2 = _count * 100
            type = 'create' if stock['holdings'] == 0 else 'buy'

            # 当前股票持仓
            stock['holdings'] = stock['holdings'] + _count2

            # 重置剩余资金
            result['balance'] = format_float(result['balance'] - total);

            stock_record = {
                'type': type,
                'date':  date,
                'price': price,
                'count': _count2,
                'total': total,
                'balance': result['balance']
            }

            # 如果 result['records'] 中没有当前股票的记录，则初始化
            if (not result['records'].get(stock['stock_code'])):
                result['records'][stock['stock_code']] = []

            # 如果是建仓，则在 result['records'] 中插入一条空记录
            if (type == 'create'):
                result['records'][stock['stock_code']].insert(0, [])

            # 第 0 条记录必定是对应的买入记录
            result['records'][stock['stock_code']][0].insert(0, stock_record)

            # 不管是建仓还是买入，都需要将当前股票加入到 result['holdings_stocks'] 中
            result['holdings_stocks'].append(stock)

    # 修改持仓状态
    result['status'] = 'long' if len(result['holdings_stocks']) > 0 else 'short'

    # 计算市值
    if (result['status'] == 'long'):
        result['market_value'] = format_float(sum([item['holdings'] * item['price'] for item in result['holdings_stocks']]))

    # 计算总资产
    result['total_funds'] = format_float(result['balance'] + result['market_value'])



    # -------------------------

    # history_collection = client[DatabaseNames.STOCK.value][DatabaseCollectionNames.STOCKS_HISTORY.value]

    # query = {
    #     'stock_code': { '$in': codes }
    # }

    # if (start_date or end_date):
    #     query['date'] = {}

    # if (start_date):
    #     query['date']['$gte'] = start_date

    # if (end_date):
    #     query['date']['$lt'] = end_date

    # pipeline = [
    #     {
    #         "$match": query
    #     },
    #     {
    #         '$group': {
    #             '_id': '$stock_code',  # 以 stock_code 作为分组依据
    #             'data': {'$push': '$$ROOT'}  # 将每个分组的文档保存到一个数组中
    #         }
    #     },
    #     {
    #         '$project': {
    #             '_id': 0,
    #             'data': 1
    #         }
    #     }
    # ]

    # dataList = history_collection.aggregate(pipeline)
    # dataList = [convert_list_objectid_to_str(item['data']) for item in dataList]


    # def compute_task(item):
    #     data = trading(item, raw_funds)
    #     if len(data) > 0:
    #         return data

    # # 并行计算，提高计算速度
    # result = Parallel(n_jobs=-1)(delayed(compute_task)(item) for item in dataList)
    # result = [data for data in result if data is not None]

    return {
        'message': '获取成功',
        'code': 0,
        'data': result
    }