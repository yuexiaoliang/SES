import os
import inspect

import pymongo
import efinance as ef
import pandas as pd
import ta

from constants.enums import DatabaseCollectionNames, DatabaseNames

from utils.logger import Logger
from utils.format import clean_data_list
from utils.transform import transform_data
from utils.database import create_mongo_client
from .utils import create_client

from .common import update_collected_time, get_collected_time

logger = Logger(log_file=os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'logs/collector.log'))

def collect_report_dates():
    """ 采集 A 股所有报告期 """

    # 采集的数据
    df = ef.stock.get_all_report_dates()

    # 如果数据为空则跳过
    if df.empty:
        logger.error("采集 A 股所有报告期数据为空，已跳过")
        return

    [collection, client] = create_client('REPORT_DATES')

    try:
        # DataFrame 转换为字典
        data = df.to_dict('records')

        # 先清空数据库集合中的所有数据
        collection.drop()

        # 把数据插入到数据库中
        collection.insert_many(clean_data_list(transform_data(data)))

        # 更新采集时间
        update_collected_time(DatabaseCollectionNames.REPORT_DATES.value)

        print('采集 A 股所有报告期完成！')
    except pymongo.errors.BulkWriteError:
        logger.error("采集 A 股所有报告期时出错，已跳过")
    finally:
        client.close()

    return df['报告日期'].tolist()


def collect_all_company_performance(report_dates=None):
    """ 采集 A 股所有公司业绩 """

    if report_dates is None:
        # 采集 A 股所有报告期
        report_dates = collect_report_dates()

    [collection, client] = create_client('ALL_COMPANY_PERFORMANCE')

    collection.drop()

    for report_date in report_dates:

        # 采集的数据
        df = ef.stock.get_all_company_performance(report_date)

        # 如果数据为空则跳过
        if df.empty:
            logger.error(f"采集 A 股 {report_date} 所有公司业绩数据为空，已跳过")
            return

        try:
            # DataFrame 转换为字典
            data = df.to_dict('records')

            # stock_code 等于 亚华电子 的数据
            for d in data:
                d["报告日期"] = report_date
                # del d["公告日期"]


            # 把数据插入到数据库中
            collection.insert_many(clean_data_list(transform_data(data)))

            # 更新采集时间
            update_collected_time(DatabaseCollectionNames.ALL_COMPANY_PERFORMANCE.value)

            print(f'采集 A 股 {report_date} 所有公司业绩完成！')
        except pymongo.errors.BulkWriteError:
            logger.error(f"采集 A 股 {report_date} 所有公司业绩时出错，已跳过")

    print('采集 A 股所有公司业绩完成！')

    client.close()


def collect_realtime_stocks():
    """ 采集 A 股最新状况

    :Returns:
    - `list`: 所有 A 股股票代码
    """

    # 采集的数据
    df = ef.stock.get_realtime_quotes()

    # 如果数据为空则跳过
    if df.empty:
        logger.error("采集 A 股最新状况数据为空，已跳过")
        return []

    [collection, client] = create_client('STOCKS')

    try:
        # DataFrame 转换为字典
        data = df.to_dict('records')

        # 先清空数据库集合中的所有数据
        collection.drop()

        # 把数据插入到数据库中
        collection.insert_many(clean_data_list(transform_data(data)))

        # 更新采集时间
        update_collected_time(DatabaseCollectionNames.STOCKS.value)

        print('采集 A 股最新状况完成！')

        # 所有 A 股股票代码
        return df['股票代码'].tolist()
    except pymongo.errors.BulkWriteError:
        logger.error("采集 A 股最新状况时出错，已跳过")
        return []
    finally:
        client.close()


def collect_stocks(stock_codes=None):
    """ 采集 A 股基本信息 """

    if stock_codes is None:
        # 采集 A 股最新状况
        stock_codes = collect_realtime_stocks()

    # 采集的数据
    df = ef.stock.get_base_info(stock_codes)

    # 如果数据为空则跳过
    if (df.empty):
        logger.error("采集 A 股基本信息数据为空，已跳过")
        return

    [collection, client] = create_client('STOCKS')

    try:
        # DataFrame 转换为字典
        data = df.to_dict('records')

        for item in clean_data_list(transform_data(data)):
            code = item['stock_code']

            # 如果数据库中以存在具有相同code的数据，则更新数据，否则插入数据
            filter = {"code": code}
            collection.update_one(filter, {"$set": item}, upsert=True)

            print(f"【{code}】 基本信息采集完成！")

        # 更新采集时间
        update_collected_time(DatabaseCollectionNames.STOCKS.value)

        print('A 股基本信息采集完成！')
    except pymongo.errors.BulkWriteError:
        logger.error("采集 A 股基本信息时出错，已跳过")
    finally:
        client.close()


def collect_stocks_history(stock_codes=None):
    """ 采集 A 股日线数据 """

    if stock_codes is None:
        # 采集 A 股最新状况
        stock_codes = collect_realtime_stocks()

    # 采集开始时间
    start_time = get_collected_time(DatabaseCollectionNames.STOCKS_HISTORY.value)

    # 测试用
    # stock_codes = ['002103']
    # start_time = '2023-01-01'

    print(f"采集 A 股日 K 开始时间 => {start_time}")

    # 采集的数据
    stock_history_dict = ef.stock.get_quote_history(
        stock_codes, beg=start_time)

    # 如果数据为空则跳过
    if (stock_history_dict is None):
        logger.error("采集 A 股日线数据为空，已跳过")
        return

    [collection, client] = create_client('STOCKS_HISTORY')

    collection.drop()

    # 遍历采集到的数据
    for code, value in stock_history_dict.items():
        if value.empty:
            logger.error(f"【{code}】该股票采集 A 股日线数据为空，已跳过")
            continue


        try:
            # DataFrame 转换为字典
            data = value.to_dict("records")

            data = transform_data(data)

            df = pd.DataFrame(data)

            # 计算EMA、DIF、DEA、MACD
            df['ema12'] = ta.trend.ema_indicator(df['closing_price'], window=12)
            df['ema26'] = ta.trend.ema_indicator(df['closing_price'], window=26)
            df['dif'] = df['ema12'] - df['ema26']
            df['dea'] = ta.trend.ema_indicator(df['dif'], window=9)
            df['macd'] = 2 * (df['dif'] - df['dea'])

            # 计算MA5、MA10、MA20
            df['ma5'] = ta.trend.sma_indicator(df['closing_price'], window=5)
            df['ma10'] = ta.trend.sma_indicator(df['closing_price'], window=10)
            df['ma20'] = ta.trend.sma_indicator(df['closing_price'], window=20)
            df['ma30'] = ta.trend.sma_indicator(df['closing_price'], window=30)

            df = df.round(2)

            # 将计算结果转换为字典列表
            data = df.to_dict(orient='records')

            # 清洗数据
            data = clean_data_list(data)

            collection.insert_many(data)

            # for item in clean_data_list(transform_data(data)):
            #     date = item['date']
            #     code = item['stock_code']

            #     # 如果数据库中以存在具有相同code和date的数据，则更新数据，否则插入数据
            #     filter = {"code": code, "date": date}
            #     collection.update_one(
            #         filter, {"$set": item}, upsert=True)

            #     print(f"【{code}】 {date} 日数据采集完成！")

            print(f"【{code}】该股票采集 A 股日线数据完成！")
        except pymongo.errors.BulkWriteError:
            logger.error(f"【{code}】该股票 A 股日线数据插入数据库时出错，已跳过")

    # 把当前的采集时间更新到数据库中
    update_collected_time(DatabaseCollectionNames.STOCKS_HISTORY.value)
    print('采集 A 股日线数据完成！')
    client.close()


def all():
    # 采集 A 股所有报告期
    collect_report_dates()
    # 采集 A 股所有公司业绩
    collect_all_company_performance()
    # 采集 A 股最新状况
    collect_realtime_stocks()
    # 采集 A 股基本信息
    collect_stocks()
    # 采集 A 股日线数据
    collect_stocks_history()