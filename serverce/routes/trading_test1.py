import datetime
import math
import random
from joblib import Parallel, delayed
from pymongo import MongoClient
from fastapi import APIRouter, Depends
from models.stock import StockHistory
from models.trading_test import StockTestResponse, StocksTestResponse
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


def trading(data,  raw_funds: float = 10000):
    '''模拟炒股测试
    :path code: 股票代码

    :param start_date: 开始日期
    :param end_date: 结束日期
    :param raw_funds: 初始资金，默认为 10000

    :return: 测试数据
    '''

    # 0: 未持仓 1: 持仓中
    status = 0;

    # 盘中持仓时间
    intraday_holding_time = 0;

    # 交易记录
    records = []

    # 剩余资金
    balance = raw_funds

    def buy(record: StockHistory, prevRecord: StockHistory):
        nonlocal status
        nonlocal balance

        macd = record['macd']
        prevMacd = prevRecord['macd']

        if (not macd or not prevMacd):
            return

        opening = record['opening_price']
        closing = record['closing_price']

        # MACD 是否上升
        isMacdUp = macd > prevMacd;

        # 价格是否上升（跌涨辐大于 0）
        isPriceUp = record['change_percent'] > 0

        # 买入条件成立
        isEstablish = isMacdUp and isPriceUp;

        if (not isEstablish):
            return;

        # 单价
        # 当日收盘价 + (当日收盘价 - 当日开盘价) * 阈值
        price = format_float(closing + (closing - opening) * random.random())

        # 买入股票数量（手）
        _count = math.floor(balance / (price * 100));
        if (_count <= 0):
            return;

        # 总金额
        total = calculateBuyCost(_count * price * 100);

        # 动态计算买入数量以及总额
        while (total > balance):
            _count -= 1;
            total = calculateBuyCost(_count * price * 100);

        # 持仓
        holdings = _count * 100;

        # 买入成本（每股）
        _cost = format_float(total / holdings);

        # 可用资金
        available_funds = format_float(balance - holdings * _cost);
        principal = balance
        balance = available_funds

        # 状态变更为持仓中
        status = 1;

        result = {
            # 时间
            'date': record['date'],

            # 买入单价
            'price': price,

            # 买入成本
            'cost': _cost,

            # 买入数量
            'holdings': holdings,

            # 总金额
            'total': total,

            # 可用资金
            'available_funds': available_funds,

            # 本金
            'principal': principal,

            'raw': { **record },
        }

        return result;

    def sell(records, record: StockHistory, prevRecord: StockHistory):
        nonlocal status
        nonlocal intraday_holding_time
        nonlocal balance

        stopLossRatio = -0.025

        ''' 卖出
        1. 动态亏损大于 3.5%
        2. 涨跌幅下降 2.5%
        3. MACD 小于等于上一日 MACD
        '''
        if (record['change_percent'] < stopLossRatio * 100):
            buyData = records[-1]['buy']

            buyTotal, holdings = buyData['total'], buyData['holdings']

            prevClosing = prevRecord['closing_price']

            # 单价
            # 上一日收盘价 - (上一日收盘价 * 止损比例 + 上一日收盘价 * 阈值)
            price = format_float(prevClosing - (prevClosing * stopLossRatio + prevClosing * 0.003 * random.random()))

            # 盘中持仓时间
            intraday_holding_time += 1;

            # 卖出总金额
            total = calculateSellCost(price, holdings);

            # 收益率
            gain_ratio = format_float(((total - buyTotal) / buyTotal) * 100);

            # 持仓时间
            holding_time = calculateDays(buyData['date'], record['date']);

            # 可用资金
            available_funds = format_float(balance + total);

            # 利润
            profit = format_float(total - buyTotal);

            # 重置本金
            balance = available_funds

            # 重置持仓时间
            _intraday_holding_time = intraday_holding_time;
            intraday_holding_time = 0;

            status = 0

            return {
                # 时间
                'date': record['date'],

                # 卖出单价
                'price': price,

                # 卖出数量
                'holdings': holdings,

                # 总金额
                'total': total,

                # 可用资金
                'available_funds': available_funds,

                # 利润
                'profit': profit,

                # 收益率
                'gain_ratio': gain_ratio,

                # 盘中持仓时间
                'intraday_holding_time': _intraday_holding_time,

                # 持仓时间
                'holding_time': holding_time,

                'raw': { **record },
            }

    # 遍历 _list
    for index, item in enumerate(data):
        if (index < 2):
            continue

        prevItem = data[index - 1]
        if not prevItem:
            continue

        if (status == 0):
            record = buy(item, prevItem)

            if (record):
                records.append({ 'buy': record })
                continue

        if (status == 1):
            sellRecord = sell(records, item, prevItem)
            if (not sellRecord):
                continue

            record = records[-1]
            record['sell'] = sellRecord
            continue


    ''' 买入
    - 从开始日期开始，每天筛选所有符合买入条件的股票
    - 并从筛选出的股票中随机（暂定）选择一只股票买入
    - 记录股票代码、股票名称、买入日期、单价、数量、佣金、过户费、总价、剩余资金
    '''

    ''' 卖出
    - 每天计算所持有的股票是否符合卖出条件，如果符合卖出条件，则卖出
    - 记录股票代码、股票名称、卖出日期、单价、数量、佣金、过户费、印花税、总收益（亏损）、所卖股票剩余持仓、剩余资金
    - 卖出价格计算方式为：当天最高价和上一天收盘价的最高价*止损比率+止损比率*0.3
    '''

    ''' 结果
    - 将所有的买入、卖出记录按日期排序
    '''
    return records

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