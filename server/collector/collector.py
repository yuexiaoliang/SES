import os
import inspect

import pymongo
import efinance as ef

from constants.constants import DEFAULT_START_COLLECT_TIME
from constants.enums import CollectedType

from utils.logger import Logger
from utils.format import format_timestamp, get_current_time
from utils.transform import transform_data


client = pymongo.MongoClient('mongodb://localhost:27017')

db = client.stock

log_file = os.path.join(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))), 'logs/collector.log')

logger = Logger(log_file=log_file)


def update_collected_time(name):
    """ 更新采集时间

    :Parameters:
    - `type` (CollectedType): 采集类型
    """
    time = get_current_time()

    db.timestamps.update_one({"name": name}, {"$set": {"collected_timestamp": time,
                             "collected_time": format_timestamp(time, '%Y-%m-%d %H:%M:%S')}}, upsert=True)


def get_collected_time(name):
    """ 获取采集时间

    :Parameters:
    - `type` (CollectedType): 采集类型
    """
    result = db.timestamps.find_one({"name": name})

    try:
        return format_timestamp(result['collected_timestamp'])
    except:
        return DEFAULT_START_COLLECT_TIME


def collect_realtime_stocks():
    """ 采集 A 股最新状况

    :Returns:
    - `list`: 所有 A 股股票代码
    """

    # 采集的数据
    stocks_df = ef.stock.get_realtime_quotes()

    # 如果数据为空则跳过
    if stocks_df.empty:
        logger.error("采集 A 股最新状况数据为空，已跳过")
        return

    try:
        # DataFrame 转换为字典
        stocks_data = stocks_df.to_dict('records')

        # 先清空数据库集合中的所有数据
        db.stocks.drop()

        # 把数据插入到数据库中
        db.stocks.insert_many(transform_data(stocks_data))

        # 更新采集时间
        update_collected_time(CollectedType.REALTIME_STOCKS.value)

        print('采集 A 股最新状况完成！')
    except pymongo.errors.BulkWriteError:
        logger.error("采集 A 股最新状况时出错，已跳过")

    # 所有 A 股股票代码
    return stocks_df['股票代码'].tolist()


def collect_stocks(stock_codes=None):
    """ 采集 A 股基本信息 """

    if stock_codes is None:
        # 采集 A 股最新状况
        stock_codes = collect_realtime_stocks()

    # 采集的数据
    base_info_df = ef.stock.get_base_info(stock_codes)

    # 如果数据为空则跳过
    if (base_info_df.empty):
        logger.error("采集 A 股基本信息数据为空，已跳过")
        return

    try:
        # DataFrame 转换为字典
        base_info_data = base_info_df.to_dict('records')

        for item in transform_data(base_info_data):
            code = item['code']

            # 如果数据库中以存在具有相同code的数据，则更新数据，否则插入数据
            filter = {"code": code}
            db.stocks.update_one(filter, {"$set": item}, upsert=True)

            print(f"【{code}】 基本信息采集完成！")

        # 更新采集时间
        update_collected_time(CollectedType.STOCKS_BASE_INFO.value)

        print('A 股基本信息采集完成！')
    except pymongo.errors.BulkWriteError:
        logger.error("采集 A 股基本信息时出错，已跳过")


def collect_stocks_history(stock_codes=None):
    """ 采集 A 股日线数据 """

    if stock_codes is None:
        # 采集 A 股最新状况
        stock_codes = collect_realtime_stocks()

    # 采集开始时间
    start_time = get_collected_time(CollectedType.STOCKS_HISTORY.value)

    print(f"采集 A 股日 K 开始时间 => {start_time}")

    # 采集的数据
    stock_history_dict = ef.stock.get_quote_history(
        stock_codes, beg=start_time)

    # 如果数据为空则跳过
    if (stock_history_dict is None):
        logger.error("采集 A 股日线数据为空，已跳过")
        return

    # 遍历采集到的数据
    for code, value in stock_history_dict.items():
        if value.empty:
            logger.error(f"【{code}】该股票采集 A 股日线数据为空，已跳过")
            continue

        try:
            # DataFrame 转换为字典
            stock_history_data = value.to_dict("records")

            for item in transform_data(stock_history_data):
                date = item['date']
                code = item['code']

                # 如果数据库中以存在具有相同code和date的数据，则更新数据，否则插入数据
                filter = {"code": code, "date": date}
                db.stock_history.update_one(
                    filter, {"$set": item}, upsert=True)

                print(f"【{code}】 {date} 日数据采集完成！")

            print(f"【{code}】该股票采集 A 股日线数据完成！")
        except pymongo.errors.BulkWriteError:
            logger.error(f"【{code}】该股票 A 股日线数据插入数据库时出错，已跳过")

    # 把当前的采集时间更新到数据库中
    update_collected_time(CollectedType.STOCKS_HISTORY.value)

    print('采集 A 股日线数据完成！')


def start():
    stock_codes = collect_realtime_stocks()
    if (not stock_codes or len(stock_codes) == 0):
        return

    collect_stocks(stock_codes)

    collect_stocks_history(stock_codes)

    client.close()
