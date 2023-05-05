import datetime
import time
from constants import column_mapping


def get_current_time():
    """ 获取当前时间的时间戳 """
    return time.time()


def format_timestamp(timestamp, format='%Y%m%d'):
    """ 格式化时间戳 """
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    return dt_obj.strftime(format)


def transform_row(data_row, column_mapping=column_mapping):
    """ 将映射字典应用到数据中的一行，并返回转换后的行。 """
    return {column_mapping[k]: v for k, v in data_row.items()}


def transform_data(data, column_mapping=column_mapping):
    """ 将映射字典应用到数据中的每一行，并返回转换后的数据。 """
    return [transform_row(row, column_mapping) for row in data]
