import datetime
import math
import random
from typing import Any
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import APIRouter, Depends
from models.stock import StockResponse, StockHistoryResponse, StockHistory
from models.common import ResponseListModel, ResponseBaseModel
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

def buy(record: StockHistory, prevRecord: StockHistory, available_funds):
    macd = record['macd']
    prevMacd = prevRecord['macd']

    if (not macd or not prevMacd):
        return

    # MACD 是否上升
    isMacdUp = macd > prevMacd;

    # 买入条件成立
    isEstablish =  isMacdUp;

    if (not isEstablish):
        return;

    price = calculatePrice(record);

    # 买入股票数量（手）
    _count = math.floor(available_funds / (price * 100));
    if (_count <= 0):
        return;

    # 总金额
    total = calculateBuyCost(_count * price * 100);

    # 动态计算买入数量以及总额
    while (total > available_funds):
      _count -= 1;
      total = calculateBuyCost(_count * price * 100);

    # 持仓
    holdings = _count * 100;

    # 买入成本（每股）
    _cost = format_float(total / holdings);

    # 可用资金
    available_funds = format_float(available_funds - holdings * _cost);

    # 状态变更为持仓中
    status = 1;

    result = {
        # 时间
        'date': record['date'],

        # 买入单价
        price: price,

        # 买入成本
        'cost': _cost,

        # 买入数量
        'holdings': holdings,

        # 总金额
        'total': total,

        # 可用资金
        'available_funds': available_funds,

        # 交易类型
        'type': "买入",

        'raw': { **record },
    }


    return result;

def sell(records, record: StockHistory, prevRecord: StockHistory):
    print(records[-1])
    buyData = records[-1]['buy']

    buyTotal, holdings, available_funds = buyData['total'], buyData['holdings'], buyData['available_funds']

    # 单价
    price = calculatePrice(record)

    # 盘中持仓时间
    # intraday_holding_time += 1;

    # 卖出总金额
    total = calculateSellCost(price, holdings);

    # 收益率
    gain_ratio = format_float(((total - buyTotal) / buyTotal) * 100);

    macd  = record['macd'];
    prevMacd = prevRecord['macd']

    ''' 卖出
    1. 动态亏损大于 3.5%
    2. MACD 小于等于上一日 MACD
    '''
    if (gain_ratio < -3.5 or macd <= prevMacd):
        # 持仓时间
        holding_time = calculateDays(buyData['date'], record['date']);

        # 可用资金
        available_funds = format_float(available_funds + total);

        # 利润
        # profit = format_float(available_funds - principal);

        # 本金
        # principal = available_funds;

        # 重置持仓时间
        # _intraday_holding_time = intraday_holding_time;
        # intraday_holding_time = 0;

        return {
            # 时间
            'date': record['date'],

            # 卖出单价
            'price': price,

            # 卖出数量
            # 'holdings': holdings,

            # 总金额
            'total': total,

            # 可用资金
            'available_funds': available_funds,

            # 本金
            # 'principal': principal,

            # 利润
            # 'profit': profit,

            # 收益率
            'gain_ratio': gain_ratio,

            # 交易类型
            'type': "卖出",

            # 盘中持仓时间
            # 'intraday_holding_time': _intraday_holding_time,

            # 持仓时间
            'holding_time': holding_time,

            'raw': { **record },
        }


class StockTestResponse(ResponseBaseModel):
    class config:
        title = "股票交易测试 Response"

    data: Any

@router.get('/{code}', name='单只股票模拟炒股测试', response_model=StockTestResponse)
def test_all(code: str, start_date:str = '', end_date: str = '', raw_funds: float = 10000, client: MongoClient = Depends(get_mongo_client)):
    '''模拟炒股测试
    :path code: 股票代码

    :param start_date: 开始日期
    :param end_date: 结束日期
    :param raw_funds: 初始资金，默认为 10000

    :return: 测试数据
    '''
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
        return {"message": "未找到符合条件的数据", "code": 0, "data": []}

    _list = convert_list_objectid_to_str(list(cursor))
    # _list = list(cursor)

    # 0: 未持仓 1: 持仓中
    status = 0;

    # 所有持仓的股票 - {code: 总数}
    holding_stocks = []

    # 交易记录
    records = []

    # 剩余资金
    balance = raw_funds

    # 遍历 _list
    for index, item in enumerate(_list):

        if (index < 2):
            continue

        prevItem = _list[index - 1]

        if (status == 0):
            record = buy(item, prevItem, balance)

            if (record):
                records.append({ 'buy': record })
                status = 1
                continue

        if (status == 1):
            sellRecord = sell(records, item, prevItem)
            if (not sellRecord):
                continue

            record = records[-1]
            record['sell'] = sellRecord
            status = 0
            continue

    print(records)


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

    return {
        'message': '获取成功',
        'code': 200,
        'data': records
    }
